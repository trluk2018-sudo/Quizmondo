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


class DailyChallengeScore(db.Model):
    """One attempt at one day's challenge.

    Kept apart from MiniGameScore, which holds a single lifetime best per game
    and so cannot carry a row per day. Here the key is the day itself, for
    example 'crossword-2026-10-28', so each day has its own table of results.
    """
    __tablename__ = 'daily_challenge_scores'
    __table_args__ = (
        db.UniqueConstraint('player_session', 'challenge_key', name='uq_daily_player'),
    )

    id = db.Column(db.Integer, primary_key=True)
    player_session = db.Column(db.String(64), index=True, nullable=False)
    challenge_key = db.Column(db.String(60), index=True, nullable=False)
    challenge_date = db.Column(db.Date, index=True, nullable=False)
    display_name = db.Column(db.String(80), default='Player')
    avatar_key = db.Column(db.String(40), default='quizzy')
    score = db.Column(db.Integer, default=0)
    seconds_taken = db.Column(db.Integer, default=0)
    solved = db.Column(db.Boolean, default=False)
    played_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def best_score(self) -> int:
        """Alias so the shared leaderboard panel can render either kind of row."""
        return self.score or 0

    def to_dict(self) -> dict:
        return {
            'display_name': self.display_name,
            'avatar_key': self.avatar_key,
            'score': self.score or 0,
            'seconds_taken': self.seconds_taken or 0,
            'solved': bool(self.solved),
        }
