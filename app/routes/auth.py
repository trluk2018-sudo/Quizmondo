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

    if not sso_secret or not token:
        flash('SSO token or secret missing.', 'error')
        return redirect(url_for('auth.login'))

    data = None
    # 1. Attempt standard itsdangerous signed token (Kangcono cross-instance-sso format)
    try:
        from itsdangerous import URLSafeTimedSerializer, BadData, SignatureExpired
        serializer = URLSafeTimedSerializer(sso_secret, salt='cross-instance-sso')
        try:
            data = serializer.loads(token, max_age=300)  # 5-minute validity window
        except SignatureExpired:
            flash("That sign-in link has expired. Click 'Log in as' again from the control plane.", "error")
            return redirect(url_for('auth.login'))
        except BadData:
            data = None
    except Exception:
        data = None

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

    uname = data.get('u') or 'admin'
    user = User.query.filter_by(username=uname).first()
    if not user:
        user = User(username=uname, email=f"{uname}@sitebuilder.local", role='admin')
        user.set_password(secrets.token_urlsafe(16))
        db.session.add(user)
        db.session.commit()

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

