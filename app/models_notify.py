"""A record of which duels we have already chased, so we chase them once.

Its own module, like models_mail and models_quiz_memory, so models.py stays
untouched.

Without this, a nightly run would mail the same person about the same stalled
duel every single night, which is how a helpful reminder turns into something
people filter.
"""
from datetime import datetime, timedelta

from .models import db

# How long before the same match may be chased again. A stalled duel is not
# more urgent on day eight than it was on day seven.
COOLDOWN_DAYS = 7
# How many times one match is ever worth chasing. After this it is not
# forgotten, it is abandoned, and more mail will not change that.
MAX_SENDS = 2


class MatchNudge(db.Model):
    """When this match was last chased, and how often."""
    __tablename__ = 'match_nudges'

    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, unique=True, index=True, nullable=False)
    last_sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    sends = db.Column(db.Integer, default=0)

    @staticmethod
    def may_send(match_id, cooldown_days=COOLDOWN_DAYS, max_sends=MAX_SENDS):
        row = MatchNudge.query.filter_by(match_id=match_id).first()
        if not row:
            return True
        if (row.sends or 0) >= max_sends:
            return False
        if not row.last_sent_at:
            return True
        return datetime.utcnow() - row.last_sent_at >= timedelta(days=cooldown_days)

    @staticmethod
    def record(match_id):
        row = MatchNudge.query.filter_by(match_id=match_id).first()
        if not row:
            row = MatchNudge(match_id=match_id, sends=0)
            db.session.add(row)
        row.sends = (row.sends or 0) + 1
        row.last_sent_at = datetime.utcnow()
        db.session.commit()
