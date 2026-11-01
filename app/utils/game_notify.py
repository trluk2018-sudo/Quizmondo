"""Reminders about duels that have gone quiet.

The in-app WhatsApp nudge only works while somebody is sitting in front of the
app at the right moment. A forgotten duel is exactly the case where nobody is:
there is no one there to tap a share button, so the only thing that can reach
them is mail the server sends on its own.

Two rules shape everything here. We chase the player whose turn it is, not
both -- there is always a current_turn, and telling two people that somebody
ought to do something is how nothing gets done. And we only send when BOTH
players have a confirmed address, so a reminder never sends somebody back to a
duel whose opponent we have no way of reaching, and never names a player who
has not confirmed they want to be in our mail.

Nothing runs on a timer by itself; the app has no scheduler. Admin has a Send
Now button, and there is a token endpoint a cron job can call.
"""
from datetime import datetime, timedelta

from ..models import db, ArenaMatch, PlayerProfile, User, SiteSetting
from ..models_mail import AccountEmail
from ..models_notify import MatchNudge
from . import mail

# Defaults; admin can change the first two.
DEFAULT_STALE_DAYS = 3
DEFAULT_ENABLED = '0'


def settings():
    """What admin has chosen, with sane fallbacks."""
    raw = SiteSetting.get_all()
    try:
        stale_days = int(raw.get('game_notify_stale_days') or DEFAULT_STALE_DAYS)
    except (TypeError, ValueError):
        stale_days = DEFAULT_STALE_DAYS
    return {
        'enabled': (raw.get('game_notify_enabled') or DEFAULT_ENABLED) == '1',
        'stale_days': max(1, stale_days),
        'cron_token': raw.get('game_notify_token') or '',
    }


def _confirmed_email(session_key):
    """The confirmed address behind a player session, or None.

    None covers every way a player can be unreachable: a guest with no
    account, an account that never gave an address, and an address that was
    given but never confirmed.
    """
    if not session_key:
        return None
    profile = PlayerProfile.query.filter_by(session_key=session_key).first()
    if not profile or not profile.user_id:
        return None
    if profile.is_banned or profile.is_paused or profile.is_anonymised:
        return None
    row = AccountEmail.query.filter_by(user_id=profile.user_id).first()
    if not row or not row.confirmed_at or not row.email:
        return None
    return {'email': row.email, 'name': profile.display_name, 'user_id': profile.user_id}


def pending(stale_days=None, ignore_cooldown=False):
    """Every stalled duel we could legitimately write about.

    Returns a list of dicts rather than sending anything, so admin can see
    exactly who would be mailed before a single message goes out.
    """
    conf = settings()
    days = stale_days if stale_days is not None else conf['stale_days']
    cutoff = datetime.utcnow() - timedelta(days=days)

    matches = ArenaMatch.query.filter(
        ArenaMatch.status.in_(['waiting', 'in_progress']),
        ArenaMatch.updated_at <= cutoff,
    ).order_by(ArenaMatch.updated_at.asc()).all()

    out = []
    for match in matches:
        if match.is_bot:
            # Nobody is waiting on the other side of a bot duel, and the
            # player did not forget it so much as leave it.
            continue
        p1 = _confirmed_email(match.player1_session)
        p2 = _confirmed_email(match.player2_session)
        if not p1 or not p2:
            continue
        try:
            turn = match.expected_turn()
        except Exception:
            turn = match.current_turn or 1
        target, other = (p1, p2) if turn == 1 else (p2, p1)
        if not ignore_cooldown and not MatchNudge.may_send(match.id):
            continue
        idle_days = (datetime.utcnow() - (match.updated_at or match.created_at)).days
        out.append({
            'match': match,
            'match_code': match.match_code,
            'to': target,
            'opponent': other,
            'round': match.current_round,
            'idle_days': idle_days,
        })
    return out


def compose(item, base_url):
    """The reminder itself. Said once, plainly, with the link to act on."""
    you = item['to']['name']
    them = item['opponent']['name']
    link = '%s/arena/match/%s' % (base_url.rstrip('/'), item['match_code'])
    subject = "%s is still waiting on your move" % them
    body = (
        "Hi %s,\n\n"
        "Your duel with %s has been sitting at round %d for %d days, and it is "
        "your turn.\n\n"
        "Three questions is all it takes to put the ball back in their court:\n"
        "%s\n\n"
        "If you would rather leave it, you can simply ignore this -- we will "
        "not keep asking.\n\n"
        "- Quizmondo\n"
    ) % (you, them, item['round'], item['idle_days'], link)
    return subject, body


def run(base_url, dry_run=False, stale_days=None):
    """Send the reminders. Returns a summary worth showing an operator."""
    conf = settings()
    result = {'enabled': conf['enabled'], 'sent': 0, 'failed': 0,
              'skipped': 0, 'items': [], 'errors': []}

    if not conf['enabled'] and not dry_run:
        result['errors'].append('Game notifications are switched off.')
        return result
    if not mail.mail_ready() and not dry_run:
        result['errors'].append('No outgoing mail account is set up yet.')
        return result

    for item in pending(stale_days=stale_days):
        subject, body = compose(item, base_url)
        row = {'to': item['to']['email'], 'name': item['to']['name'],
               'opponent': item['opponent']['name'], 'match': item['match_code'],
               'idle_days': item['idle_days'], 'subject': subject}
        if dry_run:
            row['status'] = 'would send'
            result['items'].append(row)
            continue
        try:
            ok = mail.send(item['to']['email'], subject, body)
        except Exception as exc:                      # a bad address must not
            ok, exc_text = False, str(exc)            # stop the rest of the run
            result['errors'].append('%s: %s' % (item['match_code'], exc_text))
        if ok:
            MatchNudge.record(item['match'].id)
            result['sent'] += 1
            row['status'] = 'sent'
        else:
            result['failed'] += 1
            row['status'] = 'failed'
        result['items'].append(row)

    db.session.commit()
    return result
