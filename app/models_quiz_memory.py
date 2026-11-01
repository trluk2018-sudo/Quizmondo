"""What questions a player has been asked lately.

Kept in its own module, like models_mail and models_games, so this can land
without touching models.py.

This started life in the Flask session, which worked but was per-browser: the
same account on a phone and a laptop kept two separate lists, and clearing
cookies wiped it. Signed-in players get a row here instead, so the memory
follows the account between devices and survives a new browser. Guests still
use the session, because a guest has no identity to hang a row on -- and that
is one more reason to make an account rather than a gap worth closing.

One row per account holding a JSON list, rather than a row per question seen.
The list is capped and only ever read whole, so a table that grows by a row a
question would cost a great deal and buy nothing.
"""
import json
from datetime import datetime

from .models import db

# How many questions back a player is protected from seeing a repeat. Big
# enough to cover an evening's play, small enough that a thin category is not
# exhausted by it -- and when one is, the caller tops up from the full pool
# rather than running dry.
MEMORY_LIMIT = 60


class QuestionMemory(db.Model):
    """The recently-asked question ids for one account."""
    __tablename__ = 'question_memory'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, index=True, nullable=False)
    seen_json = db.Column(db.Text, default='[]')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def recent(user_id):
        """The ids this account has been asked lately, newest first."""
        if not user_id:
            return []
        row = QuestionMemory.query.filter_by(user_id=user_id).first()
        if not row:
            return []
        try:
            return [int(qid) for qid in json.loads(row.seen_json or '[]')]
        except (TypeError, ValueError):
            # A row we cannot read is worth no more than no row at all, and a
            # player mid-game should not meet a traceback over it.
            return []

    @staticmethod
    def remember(user_id, ids, limit=MEMORY_LIMIT):
        """Push these to the front of the list, keeping it to `limit`."""
        if not user_id or not ids:
            return
        fresh = [int(qid) for qid in ids]
        kept = [qid for qid in QuestionMemory.recent(user_id) if qid not in fresh]
        merged = (fresh + kept)[:limit]

        row = QuestionMemory.query.filter_by(user_id=user_id).first()
        if not row:
            row = QuestionMemory(user_id=user_id)
            db.session.add(row)
        row.seen_json = json.dumps(merged)
        row.updated_at = datetime.utcnow()
        db.session.commit()
