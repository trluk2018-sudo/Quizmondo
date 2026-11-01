"""Proving an account's email address.

Registration already collects an address; this is what turns that claim into
something the site can rely on for a password reset or a league invite.

It deliberately stands on its own. Nothing here hooks into registration, so
the flow works today without changes to the Arena: a signed in player whose
address is unconfirmed sees a banner, presses the button, gets the email and
follows the link. Sending the first email automatically at registration is one
call to send_confirmation() in the registration route whenever its owner wants
to add it.
"""
from datetime import datetime

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from ..models import db, User, SiteSetting
from ..models_mail import AccountEmail, EmailToken, RESEND_SECONDS
from ..utils import mail

account_bp = Blueprint('account', __name__, url_prefix='/account')


def send_confirmation(user) -> tuple:
    """Issue a fresh link and email it. Returns (sent, reason-if-not)."""
    if not user or not user.email:
        return False, 'That account has no email address.'
    row = AccountEmail.for_user(user)
    if row.confirmed:
        return False, 'That address is already confirmed.'
    if not row.may_resend:
        return False, ('Another email has just gone out. Give it %d seconds before '
                       'asking again.' % RESEND_SECONDS)
    if not mail.mail_ready():
        return False, 'Email is not set up on this site yet.'

    # The address may have changed since the row was made.
    row.email = (user.email or '').lower()
    raw = EmailToken.issue(user.id, 'confirm')
    link = url_for('account.confirm', token=raw, _external=True)
    sent, why = mail.send_confirmation(row.email, user.username, link)
    if sent:
        row.last_sent_at = datetime.utcnow()
        row.sends = (row.sends or 0) + 1
        db.session.commit()
        return True, None
    return False, why


# Somebody who has just signed up is not asked to go and read their email: they
# came here to play. They get this long to play first, and then they are asked
# -- in the same session, rather than waiting for a sign-in that may never come
# round again.
FRESH_SIGNUP_MINUTES = 15

ASKED = 'qm_confirm_asked'


def confirmation_state():
    """Whether to put the confirm prompt up, and what it should say.

    None means say nothing: a guest, an address already confirmed, the session
    that created the account, or a session that has been asked once already.
    """
    user_id = session.get('user_id')
    if not user_id:
        return None
    user = db.session.get(User, user_id)
    if not user or not user.email:
        return None

    row = AccountEmail.query.filter_by(user_id=user.id).first()
    if row and row.confirmed:
        session.pop(ASKED, None)
        return None

    # How long ago they signed up, not whether this is the signing-up session.
    # Deciding it once per session meant a browser that never closed never
    # asked at all, which is how an account could play for weeks unconfirmed.
    age = (datetime.utcnow() - (user.created_at or datetime.utcnow())).total_seconds()
    if age < FRESH_SIGNUP_MINUTES * 60:
        return None            # they only just signed up: let them play

    if session.get(ASKED):
        return None            # asked once this visit, which is enough

    return {
        'email': user.email,
        'name': user.username,
        'sends': (row.sends if row else 0) or 0,
        'required': SiteSetting.get('require_email_confirm') == '1',
    }


@account_bp.before_app_request
def prepare_confirm_prompt():
    """Work out once per request whether the prompt is due.

    Done here rather than in a context processor so that marking the session as
    asked happens once, not once per template rendered.
    """
    g.confirm_prompt = None
    if request.endpoint in ('static', 'account.confirm', 'account.confirm_send'):
        return
    try:
        state = confirmation_state()
    except Exception:
        # A database that predates this feature has no table to read, and that
        # must not take every page down with it.
        state = None
    if state:
        session[ASKED] = True
        g.confirm_prompt = state


@account_bp.app_context_processor
def inject_confirmation():
    """Available on every page, so the prompt can live in the base template."""
    return {'confirm_prompt': getattr(g, 'confirm_prompt', None)}


# A reset link can take an account over, so it lives a fraction as long as a
# confirmation link.
RESET_HOURS = 2


@account_bp.route('/forgot', methods=['GET', 'POST'])
def forgot_pin():
    """Ask for a reset link. This is what confirming an address buys you.

    The answer is the same whether or not the address is on an account, and
    whether or not it was ever confirmed. Anything else turns this page into a
    way of asking the site which addresses it knows.
    """
    SAME_ANSWER = ('If that address is on a confirmed account, a reset link is '
                   'on its way. It expires in %d hours.' % RESET_HOURS)

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        if email:
            row = AccountEmail.query.filter(
                db.func.lower(AccountEmail.email) == email,
                AccountEmail.confirmed_at.isnot(None),
            ).first()
            # An unconfirmed address gets nothing: the whole point of
            # confirming is that this is what it unlocks.
            if row and row.may_resend and mail.mail_ready():
                user = db.session.get(User, row.user_id)
                if user and user.is_active:
                    raw = EmailToken.issue(user.id, 'reset', hours=RESET_HOURS)
                    link = url_for('account.reset_pin', token=raw, _external=True)
                    sent, _why = mail.send_pin_reset(row.email, user.username,
                                                     link, RESET_HOURS)
                    if sent:
                        row.last_sent_at = datetime.utcnow()
                        db.session.commit()
        flash(SAME_ANSWER, 'success')
        return redirect(url_for('account.forgot_pin'))

    return render_template('themes/quizhub/account_forgot.html',
                           mail_ready=mail.mail_ready())


@account_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_pin(token):
    """Set a new PIN from a link. One use, then the link is spent."""
    # The token is only spent on POST. Checking it on GET as well would burn a
    # one-use link just by opening the page.
    if request.method == 'POST':
        claimed = EmailToken.claim(token, 'reset')
        if not claimed:
            flash('That link has expired or has already been used. Ask for a new one.', 'error')
            return redirect(url_for('account.forgot_pin'))
        user = db.session.get(User, claimed.user_id)
        if not user or not user.is_active:
            flash('That account is no longer available.', 'error')
            return redirect(url_for('account.forgot_pin'))

        pin = (request.form.get('pin') or '').strip()
        again = (request.form.get('pin_confirm') or '').strip()
        if not (pin.isdigit() and len(pin) == 6):
            flash('A PIN is six digits.', 'error')
            return redirect(url_for('account.reset_pin', token=token))
        if pin != again:
            flash('Those two PINs did not match.', 'error')
            return redirect(url_for('account.reset_pin', token=token))

        user.set_password(pin)
        db.session.commit()
        flash('That is your new PIN. Sign in with it now.', 'success')
        return redirect(url_for('arena.player_login'))

    return render_template('themes/quizhub/account_reset.html', token=token)


@account_bp.route('/confirm/send', methods=['POST'])
def confirm_send():
    user = db.session.get(User, session.get('user_id'))
    if not user:
        flash('Sign in first and we will send the link.', 'error')
        return redirect(url_for('arena.player_login'))
    sent, why = send_confirmation(user)
    if sent:
        flash('Check %s for a link to confirm your account.' % user.email, 'success')
    else:
        flash(why, 'error')
    return redirect(request.referrer or url_for('arena.dashboard'))


@account_bp.route('/confirm/<token>')
def confirm(token):
    """Spend a confirmation link.

    Signing in is not required: somebody opening the link in their phone's
    mail app is often not the browser that signed up, and refusing them there
    is how confirmation emails get abandoned.
    """
    row = EmailToken.claim(token, 'confirm')
    if row is None:
        db.session.rollback()
        return render_template('themes/quizhub/account_confirm.html',
                               ok=False,
                               heading='That link has expired',
                               detail=('Confirmation links work once and last 48 hours. '
                                       'Sign in and ask for a fresh one.')), 400

    user = db.session.get(User, row.user_id)
    if user is None:
        db.session.rollback()
        return render_template('themes/quizhub/account_confirm.html',
                               ok=False,
                               heading='That account is gone',
                               detail='The account this link belonged to no longer exists.'), 404

    status = AccountEmail.for_user(user)
    if not status.confirmed:
        status.confirmed_at = datetime.utcnow()
    status.email = (user.email or '').lower()
    db.session.commit()

    return render_template('themes/quizhub/account_confirm.html',
                           ok=True,
                           heading='Confirmed',
                           detail=('%s is yours. Your scores, coins and streak are saved '
                                   'for good now.' % user.email),
                           username=user.username)
