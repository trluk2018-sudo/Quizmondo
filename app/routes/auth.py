import os
import hmac
import hashlib
import time
import secrets
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from ..models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix='/admin')


@auth_bp.context_processor
def inject_admin_chrome():
    """Pages here render admin/base.html, which the Admin blueprint feeds.

    Its sidebar reads admin_quick_pages. A context processor only runs for its
    own blueprint, so without this the profile page raises an undefined
    variable and returns a 500 instead of a form.
    """
    from .admin import inject_admin_quick_pages
    return inject_admin_quick_pages()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login', next=request.url))
        if session.get('user_role') not in ('admin', 'super_admin'):
            flash('Access restricted to administrators.', 'error')
            return redirect(url_for('public.home'))
        return f(*args, **kwargs)
    return decorated_function


def handle_sso():
    """Handle Single Sign-On from the SaaS Control Plane ("Log in as").
    Compatible with itsdangerous URLSafeTimedSerializer tokens (salt='cross-instance-sso')
    and fallback legacy HMAC tokens.
    """
    token = request.args.get('token', '').strip()
    sso_secret = current_app.config.get('APP_SSO_SECRET') or current_app.config.get('SECRET_KEY', '')

    if not token or (not sso_secret and not token.startswith('ed25519.')):
        flash('SSO token or secret missing.', 'error')
        return redirect(url_for('auth.login'))

    data = None
    # 0. Attempt asymmetric Ed25519 token signed by Kangcono Verify (local PC companion)
    if token.startswith('ed25519.'):
        from ..utils.ed25519_sso import verify_ed25519_sso_token
        data, err = verify_ed25519_sso_token(token, expected_scope='tenant', expected_aud=[request.host])
        if err == 'expired':
            flash("That Kangcono Verify sign-in link has expired (60s window).", "error")
            return redirect(url_for('auth.login'))
        elif err:
            flash("Could not verify Kangcono Verify Ed25519 signature.", "error")
            return redirect(url_for('auth.login'))

    # 1. Attempt standard itsdangerous signed token (Kangcono cross-instance-sso format)
    if not data:
        from itsdangerous import URLSafeTimedSerializer, BadData, SignatureExpired
        from sqlalchemy.exc import IntegrityError
        import time, hashlib
        # Determine all candidate subdomains for this tenant to handle variations
        candidate_subdomains = set()
        for cand in [
            os.environ.get('APP_SUBDOMAIN'),
            os.environ.get('SUBDOMAIN'),
            current_app.config.get('SUBDOMAIN'),
            request.host.split(':')[0].split('.')[0],
        ]:
            if cand:
                c = cand.strip().lower()
                candidate_subdomains.add(c)
                candidate_subdomains.add(c.replace('-', ''))
                candidate_subdomains.add(c.replace('_', ''))

        # Each company gets its own key (derived from master APP_SSO_SECRET plus site name).
        # Master APP_SSO_SECRET is NEVER accepted directly as a decryption key (M2).
        candidate_keys = [
            hashlib.sha256(f"{sso_secret}:{sub}".encode('utf-8')).hexdigest()
            for sub in candidate_subdomains
        ]

        for key_candidate in candidate_keys:
            try:
                serializer = URLSafeTimedSerializer(key_candidate, salt='cross-instance-sso')
                data = serializer.loads(token, max_age=60)  # Clamped to 60s
                break
            except Exception:
                continue

        if data:
            # 1. Site isolation: require site identity (sub / aud) and check destination (M2)
            token_sub = (data.get('sub') or data.get('aud') or '').strip().lower()
            if not token_sub:
                current_app.logger.warning("SSO token missing required site identity (sub/aud)")
                flash("That sign-in link is missing site identity and cannot be used.", "error")
                return redirect(url_for('auth.login'))

            req_host = (request.host or '').lower().split(':')[0]
            site_matches = (
                token_sub in candidate_subdomains
                or token_sub.replace('-', '') in candidate_subdomains
                or token_sub in req_host
            )
            if not site_matches:
                current_app.logger.warning(f"SSO site mismatch: token for '{token_sub}', host is '{request.host}'")
                flash("That sign-in link was issued for a different site and cannot be used here.", "error")
                return redirect(url_for('auth.login'))

            # 2. Once-only: single-use nonce
            nonce = data.get('nonce') or hashlib.sha256(token.encode('utf-8')).hexdigest()
            from ..models import SsoUsedNonce
            SsoUsedNonce.__table__.create(bind=db.engine, checkfirst=True)
            now_ts = int(time.time())
            try:
                SsoUsedNonce.query.filter(SsoUsedNonce.expires_at < now_ts).delete(synchronize_session=False)
                db.session.add(SsoUsedNonce(nonce=str(nonce)[:64], expires_at=now_ts + 300))
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("That sign-in link has already been used. Please request a fresh link.", "error")
                return redirect(url_for('auth.login'))
            except Exception:
                db.session.rollback()
                if SsoUsedNonce.query.filter_by(nonce=str(nonce)[:64]).first() is not None:
                    flash("That sign-in link has already been used. Please request a fresh link.", "error")
                    return redirect(url_for('auth.login'))

    # 2. Fallback to legacy HMAC verification if timestamp provided
    if not data:
        timestamp = request.args.get('ts')
        username = request.args.get('user', 'admin')
        if timestamp:
            try:
                ts = int(timestamp)
                if abs(time.time() - ts) <= 300:
                    msg = f"{username}:{timestamp}".encode('utf-8')
                    expected = hmac.new(sso_secret.encode('utf-8'), msg, hashlib.sha256).hexdigest()
                    if hmac.compare_digest(expected, token):
                        data = {'u': username, 'ret': None}
            except Exception:
                pass

    if not data:
        current_app.logger.warning("SSO signature verification failed.")
        flash("Invalid SSO signature. Check that APP_SSO_SECRET matches the control plane.", "error")
        return redirect(url_for('auth.login'))

    uname = (data.get('u') or '').strip()
    user = User.query.filter_by(username=uname).first() if (uname and uname != '@auto') else None
    if not user:
        user = User.query.filter(User.role.in_(['super_admin', 'admin'])).order_by(User.id.asc()).first()
    if not user:
        current_app.logger.error("SSO rejected: No administrative account found in database to sign into.")
        flash("Sign-in failed: No administrative account exists on this instance to sign into.", "error")
        return redirect(url_for('auth.login'))

    from ..utils.support_access import get_support_access_status
    sa_status = get_support_access_status(db, is_quizmondo=True)
    if not sa_status.get('is_active'):
        if sa_status.get('reason') == 'disabled_by_owner':
            flash("Support access has been disabled by the site owner. Operator sign-in is not permitted.", "error")
        else:
            flash("Support access window has expired. The site owner must enable support access in Settings.", "error")
        return redirect(url_for('auth.login'))

    session['user_id'] = user.id
    session['username'] = user.username
    session['user_role'] = user.role
    session['impersonation'] = True
    session['platform_return'] = data.get('ret')
    flash(f"Signed in as {user.username} via SaaS Control Plane.", "success")
    return redirect(url_for('admin.dashboard'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = request.form.get('password') or ''

        # Repeated wrong guesses are made expensive. See utils/throttle.py for
        # why this is worth more here than a second factor would be.
        from ..utils import throttle
        guard = throttle.key_for(username, request.remote_addr)
        waiting = throttle.locked_for(guard)
        if waiting:
            flash('Too many failed attempts. Try again in %s.' % throttle.describe(waiting),
                  'error')
            return render_template('auth/login.html')

        user = User.query.filter((User.username == username) | (User.email == username)).first()

        if user and user.check_password(password) and user.is_active:
            throttle.clear(guard)
            # Quizmondo 2FA: OFF by default. Only prompt if explicitly enabled by admin.
            if getattr(user, 'totp_enabled', False) and user.totp_secret:
                session['pending_2fa_user_id'] = user.id
                session['pending_2fa_next'] = request.args.get('next')
                return redirect(url_for('auth.verify_2fa'))

            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_role'] = user.role or 'player'
            session['is_creator'] = user.role in ('super_admin', 'admin', 'quizmaster', 'creator')
            flash('Welcome back, ' + user.username, 'success')
            next_url = request.args.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            if user.role in ('admin', 'super_admin'):
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('arena.dashboard'))
        else:
            throttle.record_failure(guard)
            flash('Invalid username or password.', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/sso')
def sso():
    return handle_sso()


def end_impersonation_handler():
    """Terminate the impersonation session and return to SaaS Control Plane."""
    ret = session.get('platform_return')
    session.clear()
    flash('Support session ended.', 'info')
    if ret:
        return redirect(ret)
    return redirect(url_for('auth.login'))


@auth_bp.route('/end-impersonation')
def end_impersonation():
    return end_impersonation_handler()


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = db.session.get(User, session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    is_impersonation = session.get('impersonation', False)

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        current_password = request.form.get('current_password') or ''
        new_password = request.form.get('new_password') or ''
        confirm_password = request.form.get('confirm_password') or ''

        if email and email.lower() != (user.email or '').lower():
            user.email = email
            # A new address has not been proved, whatever the old one managed.
            try:
                from ..models_mail import AccountEmail
                row = AccountEmail.query.filter_by(user_id=user.id).first()
                if row:
                    row.email = email.lower()
                    row.confirmed_at = None
                    row.last_sent_at = None
            except Exception:
                pass
        elif email:
            user.email = email

        if new_password:
            # A player's PIN protects a score; an admin's protects the site.
            from ..models import SiteSetting
            staff = (user.role or '') in ('admin', 'super_admin', 'quizmaster', 'creator')
            if staff and SiteSetting.get('staff_require_password') == '1':
                if new_password.isdigit() or len(new_password) < 10:
                    flash('Accounts with staff roles need a real password: at least 10 '
                          'characters and not just digits.', 'error')
                    return render_template('admin/profile.html', user=user,
                                           is_impersonation=is_impersonation)

            # Impersonated session can change admin password directly without knowing old random password
            if not is_impersonation and not user.check_password(current_password):
                flash('Current password is incorrect.', 'error')
                return render_template('admin/profile.html', user=user, is_impersonation=is_impersonation)

            if len(new_password) < 4:
                flash('New password / PIN must be at least 4 characters long.', 'error')
                return render_template('admin/profile.html', user=user, is_impersonation=is_impersonation)

            if new_password != confirm_password:
                flash('New passwords do not match.', 'error')
                return render_template('admin/profile.html', user=user, is_impersonation=is_impersonation)

            user.set_password(new_password)
            flash('Password updated successfully.', 'success')
        else:
            flash('Profile updated successfully.', 'success')

        db.session.commit()
        return redirect(url_for('auth.profile'))

    return render_template('admin/profile.html', user=user, is_impersonation=is_impersonation)



@auth_bp.route('/extend-support-access', methods=['POST'])
def extend_support_access_route():
    if not session.get('impersonation'):
        flash("Only active support sessions can extend the access window.", "error")
        return redirect(url_for('auth.login'))
    try:
        minutes = int(request.form.get('minutes', 60))
    except (ValueError, TypeError):
        minutes = 60
    from ..utils.support_access import extend_support_access
    st = extend_support_access(db, additional_minutes=minutes, is_quizmondo=True)
    flash(f"Support access window extended by {minutes} minutes.", "success")
    return redirect(request.referrer or url_for('admin.dashboard'))


@auth_bp.route('/support-access-toggle', methods=['POST'])
@login_required
def toggle_support_access():
    if session.get('user_role') not in ('admin', 'super_admin'):
        flash("Only site administrators can change support access settings.", "error")
        return redirect(request.referrer or url_for('admin.dashboard'))
    allow = request.form.get('allow_support') in ('1', 'on', 'true', 'True')
    persistent = request.form.get('persistent_control') in ('1', 'on', 'true', 'True')
    from ..utils.support_access import update_support_access
    st = update_support_access(db, enabled=allow, persistent=persistent, duration_minutes=60, is_quizmondo=True)
    if allow:
        if st.get('is_persistent'):
            flash("Support access enabled in Persistent Control mode.", "success")
        else:
            flash(f"Support access enabled for 60 minutes ({st.get('remaining_minutes', 60)}m remaining).", "success")
    else:
        flash("Support access disabled. SaaS Control Plane operators cannot sign in.", "info")
    return redirect(request.referrer or url_for('admin.dashboard'))


@auth_bp.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    user_id = session.get('pending_2fa_user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    user = User.query.get(user_id)
    if not user or not getattr(user, 'totp_enabled', False):
        session.pop('pending_2fa_user_id', None)
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        from ..utils.totp import verify_totp, verify_and_consume_recovery_code
        code = (request.form.get('code') or '').strip().replace(' ', '')
        good = False
        recovery_used = False

        if len(code) == 6 and code.isdigit():
            if verify_totp(user.totp_secret, code):
                good = True

        if not good and len(code) in (8, 9):
            valid_rec, updated_rec = verify_and_consume_recovery_code(code, user.totp_recovery_codes)
            if valid_rec:
                good = True
                recovery_used = True
                user.totp_recovery_codes = updated_rec
                db.session.commit()

        if good:
            next_url = session.pop('pending_2fa_next', None)
            session.pop('pending_2fa_user_id', None)
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_role'] = user.role or 'player'
            session['is_creator'] = user.role in ('super_admin', 'admin', 'quizmaster', 'creator')
            if recovery_used:
                flash('Signed in with backup recovery code. Please generate new recovery codes.', 'warning')
            else:
                flash('Two-factor verification successful.', 'success')
            return redirect(next_url or url_for('admin.dashboard'))
        else:
            flash('Invalid verification code.', 'error')

    return render_template('auth/verify_2fa.html', email=user.email, method='totp', has_totp=True)
