"""Mini game score keeping.

Kept in its own module so the mini games can evolve without touching the
Arena models. It reuses the same SQLAlchemy instance, so the table is created
by the usual db.create_all() in app/__init__.py.
"""
from datetime import datetime

from .models import db


class MiniGameScore(db.Model):
    __tablename__ = 'mini_game_scores'
    __table_args__ = (
        db.UniqueConstraint('player_session', 'game_key', name='uq_mini_game_player'),
    )

    id = db.Column(db.Integer, primary_key=True)
    player_session = db.Column(db.String(64), index=True, nullable=False)
    game_key = db.Column(db.String(40), index=True, nullable=False)
    display_name = db.Column(db.String(80), default='Player')
    avatar_key = db.Column(db.String(40), default='quizzy')
    best_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)
    plays = db.Column(db.Integer, default=0)
    best_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_played_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            'game_key': self.game_key,
            'display_name': self.display_name,
            'avatar_key': self.avatar_key,
            'best_score': self.best_score or 0,
            'last_score': self.last_score or 0,
            'plays': self.plays or 0,
        }
