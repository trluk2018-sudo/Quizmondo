"""Outgoing email.

One place for every message the site sends, so they all get the same care: a
time limit (a mail server that never answers would otherwise hang the worker
until it is killed), encryption whenever the server offers it rather than only
when a setting said so, and the Date and Message-ID headers whose absence gets
mail binned as spam by Gmail and Outlook.

Adapted from the same module in Kangcono, which has been through enough real
mail servers to know what goes wrong.

Credentials live in site settings so an operator can change them without a
deploy, except the password, which is read from the SMTP_PASSWORD environment
variable when one is set. That way the secret can be kept out of the database
and out of every backup taken of it.
"""
import os
import smtplib
import textwrap
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid

from ..models import SiteSetting

# Why the last send failed, in words an operator can act on. Shown on the
# email settings page: a failure that only reaches the server log is a failure
# nobody can fix.
LAST_ERROR = {'when': None, 'error': None}

TIMEOUT = 20

DEFAULTS = {
    'smtp_host': '',
    'smtp_port': '465',
    'smtp_user': '',
    'smtp_encryption': '',
    'smtp_from_name': 'Quizmondo',
    'smtp_from_email': '',
}


def config() -> dict:
    """The mail settings, with the password resolved from wherever it lives."""
    settings = SiteSetting.get_all()
    conf = {key: (settings.get(key) or default) for key, default in DEFAULTS.items()}
    conf['password'] = os.environ.get('SMTP_PASSWORD') or settings.get('smtp_password') or ''
    conf['password_from_env'] = bool(os.environ.get('SMTP_PASSWORD'))
    conf['from_email'] = conf['smtp_from_email'] or conf['smtp_user']
    try:
        conf['port'] = int(conf['smtp_port'])
    except (TypeError, ValueError):
        conf['port'] = 465
    # Unset means follow the port, which is right far more often than not.
    conf['encryption'] = conf['smtp_encryption'] or ('ssl' if conf['port'] == 465 else 'tls')
    return conf


def mail_ready(conf=None) -> bool:
    """True when there is enough to attempt a send."""
    conf = conf or config()
    return bool(conf['smtp_host'] and conf['smtp_user'] and conf['password'])


def _short(exc) -> str:
    text = str(exc)
    if isinstance(exc, smtplib.SMTPResponseException):
        msg = exc.smtp_error
        text = msg.decode(errors='replace') if isinstance(msg, bytes) else str(msg)
    return ' '.join(text.split())[:200]


def _explain(exc, conf) -> str:
    """Turn an SMTP exception into a sentence that says what to change."""
    host = '%s:%s' % (conf['smtp_host'], conf['port'])
    if isinstance(exc, smtplib.SMTPAuthenticationError):
        return ('%s refused the username or password (%s). Many providers need an '
                'app password rather than the normal one.' % (host, _short(exc)))
    if isinstance(exc, smtplib.SMTPSenderRefused):
        return ('%s will not send as %s (%s). The sender usually has to be the same '
                'mailbox you log in as.' % (host, conf['from_email'], _short(exc)))
    if isinstance(exc, smtplib.SMTPRecipientsRefused):
        return 'The mail server refused the recipient address (%s).' % _short(exc)
    if isinstance(exc, TimeoutError) or 'timed out' in str(exc).lower():
        return ('No answer from %s within %ds. Check the server name and port, and '
                'that this server is allowed to send mail out on that port.' % (host, TIMEOUT))
    if isinstance(exc, ConnectionRefusedError) or 'refused' in str(exc).lower():
        return 'Nothing is accepting mail at %s. Check the server name and port.' % host
    if 'ssl' in exc.__class__.__name__.lower() or 'wrong version' in str(exc).lower():
        return ('The encryption did not match at %s. Port 465 uses SSL from the start; '
                '587 and 25 start plain and upgrade. Check the port.' % host)
    if 'getaddrinfo' in str(exc) or 'Name or service not known' in str(exc):
        return 'The mail server name %s could not be found.' % conf['smtp_host']
    return '%s: %s' % (exc.__class__.__name__, _short(exc))


def deliver(msg, conf=None):
    """Send one prepared message. Returns (sent, reason-if-not)."""
    conf = conf or config()
    if not mail_ready(conf):
        LAST_ERROR.update(when=datetime.utcnow(), error='Email is not set up yet.')
        return False, LAST_ERROR['error']
    if not msg.get('Date'):
        msg['Date'] = formatdate(localtime=True)
    if not msg.get('Message-ID'):
        domain = (conf['from_email'] or '').split('@')[-1] or None
        msg['Message-ID'] = make_msgid(domain=domain)
    server = None
    try:
        if conf['encryption'] == 'ssl':
            server = smtplib.SMTP_SSL(conf['smtp_host'], conf['port'], timeout=TIMEOUT)
        else:
            server = smtplib.SMTP(conf['smtp_host'], conf['port'], timeout=TIMEOUT)
            server.ehlo()
            if conf['encryption'] != 'none' and server.has_extn('starttls'):
                server.starttls()
                server.ehlo()
        server.login(conf['smtp_user'], conf['password'])
        server.send_message(msg)
        LAST_ERROR.update(when=None, error=None)
        return True, None
    except Exception as exc:
        reason = _explain(exc, conf)
        LAST_ERROR.update(when=datetime.utcnow(), error=reason)
        print('Mail error: %s' % reason)
        return False, reason
    finally:
        if server is not None:
            try:
                server.quit()
            except Exception:
                pass


def message(to, subject, body, conf=None):
    """A plain text message from the site, addressed to one person."""
    conf = conf or config()
    msg = MIMEMultipart()
    msg['From'] = '%s <%s>' % (conf['smtp_from_name'], conf['from_email'])
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    return msg


def send(to, subject, body):
    """Send one message. Returns (sent, reason-if-not)."""
    conf = config()
    return deliver(message(to, subject, body, conf), conf)


def send_confirmation(to, display_name, link):
    """The one time email: prove the address works, then never write again."""
    conf = config()
    name = (display_name or 'there').split()[0]
    body = textwrap.dedent("""\
        Hi %s,

        Confirm your %s account by opening this link:

        %s

        It works once and expires in 48 hours. Once confirmed, your scores,
        coins and streak are saved for good, and you can take on duels and the
        daily crossword.

        If you did not sign up, ignore this email and nothing will happen.

        %s
        """) % (name, conf['smtp_from_name'], link, conf['smtp_from_name'])
    return deliver(message(to, 'Confirm your %s account' % conf['smtp_from_name'],
                           body, conf), conf)
