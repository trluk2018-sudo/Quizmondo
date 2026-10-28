"""Slowing down repeated failed sign ins.

A six digit PIN is a million combinations, which is minutes of work for a
script against an endpoint that accepts unlimited guesses. This is what closes
that, and it matters a great deal more here than a second factor would.

Counters are held in the process rather than the database, deliberately: the
SQLite file is already the busiest thing in the app during a duel or a pub
league, and a failed login is not worth a write to it. The cost is that with
several web workers each keeps its own tally, so the real allowance is roughly
the limit times the number of workers. That is still the difference between a
million guesses and a few dozen.

Attempts are counted per username and per address together, so one person
fumbling their own PIN cannot lock out anybody else.
"""
import time
from threading import Lock

_FAILURES = {}
_LOCK = Lock()

# Nothing is remembered forever: a tally older than this is simply dropped, so
# the dictionary cannot grow without bound from traffic that never returns.
FORGET_AFTER = 3600


def _settings():
    """Read the limits, falling back to sane numbers if they are unset."""
    from ..models import SiteSetting
    try:
        attempts = int(SiteSetting.get('login_max_attempts') or 8)
    except (TypeError, ValueError):
        attempts = 8
    try:
        minutes = int(SiteSetting.get('login_lockout_minutes') or 15)
    except (TypeError, ValueError):
        minutes = 15
    return max(3, attempts), max(1, minutes) * 60


def _prune(now):
    for key, (count, last) in list(_FAILURES.items()):
        if now - last > FORGET_AFTER:
            _FAILURES.pop(key, None)


def key_for(identifier, remote_addr=None) -> str:
    return '%s|%s' % ((identifier or '').strip().lower(), remote_addr or '-')


def locked_for(key) -> int:
    """Seconds still to wait, or 0 when a sign in may be attempted."""
    attempts, lockout = _settings()
    now = time.time()
    with _LOCK:
        _prune(now)
        count, last = _FAILURES.get(key, (0, 0))
    if count < attempts:
        return 0
    remaining = int(lockout - (now - last))
    return remaining if remaining > 0 else 0


def record_failure(key) -> None:
    now = time.time()
    attempts, lockout = _settings()
    with _LOCK:
        count, last = _FAILURES.get(key, (0, 0))
        # A lockout that has run its course starts the count again, rather
        # than leaving somebody one guess from being locked out for ever.
        if count >= attempts and (now - last) > lockout:
            count = 0
        _FAILURES[key] = (count + 1, now)


def clear(key) -> None:
    """Forget the failures for this key: they got in."""
    with _LOCK:
        _FAILURES.pop(key, None)


def describe(seconds) -> str:
    if seconds >= 120:
        return '%d minutes' % round(seconds / 60.0)
    if seconds >= 60:
        return 'a minute'
    return '%d seconds' % max(1, seconds)
