"""Email confirmation state and the single use links that carry it.

Kept in its own module, like models_games, so account confirmation can land
without touching models.py. Confirmation lives in its own table rather than as
a column on User for the same reason, and it reads just as well: a row here
means the address has been proved, and no row means it has not.
"""
import hashlib
import secrets
from datetime import datetime, timedelta

from .models import db

TOKEN_HOURS = 48
# A resend is one button press away, so there has to be a floor on how often
# it will actually send. Otherwise the button is a way to post mail to anybody
# whose address somebody knows.
RESEND_SECONDS = 120


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


class AccountEmail(db.Model):
    """What we know about one account's email address.

    One row per user. confirmed_at is the whole point: until it is set, the
    address is only a claim.
    """
    __tablename__ = 'account_emails'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    last_sent_at = db.Column(db.DateTime, nullable=True)
    sends = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def confirmed(self) -> bool:
        return self.confirmed_at is not None

    @property
    def may_resend(self) -> bool:
        if self.confirmed or not self.last_sent_at:
            return True
        return (datetime.utcnow() - self.last_sent_at).total_seconds() >= RESEND_SECONDS

    @classmethod
    def for_user(cls, user, create=True):
        row = cls.query.filter_by(user_id=user.id).first()
        if row is None and create:
            row = cls(user_id=user.id, email=(user.email or '').lower())
            db.session.add(row)
            db.session.flush()
        return row

    @classmethod
    def is_confirmed(cls, user_id) -> bool:
        if not user_id:
            return False
        row = cls.query.filter_by(user_id=user_id).first()
        return bool(row and row.confirmed_at)


class EmailToken(db.Model):
    """A single use link.

    Only the hash of the token is stored, so a copy of the database is not a
    pile of working confirmation links. The raw value exists just long enough
    to go into the email.
    """
    __tablename__ = 'email_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    purpose = db.Column(db.String(30), default='confirm', index=True)
    token_hash = db.Column(db.String(64), unique=True, index=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def issue(cls, user_id, purpose='confirm', hours=TOKEN_HOURS):
        """Make a new token and retire any earlier one for the same purpose.

        Returns the raw token, which is the only time it can be read.
        """
        cls.query.filter_by(user_id=user_id, purpose=purpose, used_at=None).update(
            {'used_at': datetime.utcnow()})
        raw = secrets.token_urlsafe(32)
        db.session.add(cls(user_id=user_id, purpose=purpose, token_hash=_hash(raw),
                           expires_at=datetime.utcnow() + timedelta(hours=hours)))
        db.session.commit()
        return raw

    @classmethod
    def claim(cls, raw, purpose='confirm'):
        """Spend a token. Returns the row, or None if it will not do.

        A token that has been used or has expired gives None, which is what
        makes the link work once and not forever.
        """
        if not raw:
            return None
        row = cls.query.filter_by(token_hash=_hash(raw), purpose=purpose).first()
        if row is None or row.used_at is not None:
            return None
        if row.expires_at < datetime.utcnow():
            return None
        row.used_at = datetime.utcnow()
        return row
