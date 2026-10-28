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
# came here to play. An account younger than this, first seen in this browser
# session, is treated as a fresh sign up and left alone for the whole session.
FRESH_SIGNUP_MINUTES = 30

SIGNUP_SESSION = 'qm_signup_session'
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
        session.pop(SIGNUP_SESSION, None)
        session.pop(ASKED, None)
        return None

    # First sight of this account in this browser session decides whether this
    # is the sign up itself or a later visit.
    if SIGNUP_SESSION not in session:
        age = datetime.utcnow() - (user.created_at or datetime.utcnow())
        session[SIGNUP_SESSION] = (age.total_seconds() < FRESH_SIGNUP_MINUTES * 60)
    if session.get(SIGNUP_SESSION):
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
