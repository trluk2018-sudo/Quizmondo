"""Mondo Critters: daily trivia companion pet model.

Ultra-lightweight on the server: all 100+ animated character appearances are
stored as one ~120-byte JSON blob and rendered procedurally in SVG on the client.
"""
import json
from datetime import datetime, date

from .models import db


DEFAULT_APPEARANCE = {
    'species': 'fox',
    'preset_id': 1,
    'color': '#22d3ee',
    'accent': '#f472b6',
    'hair': 'tuft',
    'hat': 'none',
    'scarf': 'striped',
}


class CritterCompanion(db.Model):
    __tablename__ = 'critter_companions'

    id = db.Column(db.Integer, primary_key=True)
    player_profile_id = db.Column(db.Integer, db.ForeignKey('player_profiles.id'), unique=True, index=True, nullable=False)
    name = db.Column(db.String(40), default='Nova')
    appearance_json = db.Column(db.Text, default=lambda: json.dumps(DEFAULT_APPEARANCE))

    # 3 core health stats (0..100). Keep all 3 above 20 to stay healthy!
    hunger = db.Column(db.Integer, default=80)
    fitness = db.Column(db.Integer, default=80)
    happiness = db.Column(db.Integer, default=80)

    status = db.Column(db.String(20), default='healthy')  # healthy | warning | sick | fainted
    care_tokens = db.Column(db.Integer, default=2)
    days_alive = db.Column(db.Integer, default=1)
    total_correct = db.Column(db.Integer, default=0)

    last_decay_date = db.Column(db.Date, default=lambda: datetime.utcnow().date())
    last_quiz_date = db.Column(db.Date, nullable=True)
    today_q_index = db.Column(db.Integer, default=0)
    today_correct = db.Column(db.Integer, default=0)
    today_wrong = db.Column(db.Integer, default=0)
    today_q_ids_json = db.Column(db.Text, default='[]')
    sick_penalty_applied = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_appearance(self) -> dict:
        try:
            data = json.loads(self.appearance_json or '{}')
            merged = dict(DEFAULT_APPEARANCE)
            merged.update({k: v for k, v in data.items() if v is not None})
            return merged
        except Exception:
            return dict(DEFAULT_APPEARANCE)

    def set_appearance(self, data: dict):
        cur = self.get_appearance()
        for k in ('species', 'preset_id', 'color', 'accent', 'hair', 'hat', 'scarf'):
            if k in data:
                cur[k] = data[k]
        self.appearance_json = json.dumps(cur)

    def get_today_q_ids(self) -> list:
        try:
            return list(json.loads(self.today_q_ids_json or '[]'))
        except Exception:
            return []

    def set_today_q_ids(self, q_ids: list):
        self.today_q_ids_json = json.dumps([int(x) for x in q_ids])

    def recalc_status(self):
        self.hunger = max(0, min(100, int(self.hunger or 0)))
        self.fitness = max(0, min(100, int(self.fitness or 0)))
        self.happiness = max(0, min(100, int(self.happiness or 0)))
        lowest = min(self.hunger, self.fitness, self.happiness)
        if lowest <= 0:
            self.status = 'fainted'
        elif self.sick_penalty_applied and lowest <= 45:
            self.status = 'sick'
        elif lowest <= 20:
            self.status = 'warning'
        else:
            self.status = 'healthy'
        return self.status

    def apply_daily_decay(self):
        """Gentle daily decay based on calendar days elapsed since last visit."""
        today = datetime.utcnow().date()
        if not self.last_decay_date:
            self.last_decay_date = today
            return False
        delta = (today - self.last_decay_date).days
        if delta <= 0:
            return False
        if self.status != 'fainted':
            # Cap decay at 4 missed days so a short holiday doesn't feel unfair if stats were high
            eff_days = min(delta, 4)
            drop = eff_days * 15
            self.hunger = max(0, (self.hunger or 0) - drop)
            self.fitness = max(0, (self.fitness or 0) - drop)
            self.happiness = max(0, (self.happiness or 0) - drop)
            if self.status != 'fainted':
                self.days_alive = (self.days_alive or 1) + delta
        self.last_decay_date = today
        self.sick_penalty_applied = False
        self.recalc_status()
        return True

    def to_dict(self) -> dict:
        today = datetime.utcnow().date()
        quiz_done_today = bool(self.last_quiz_date == today and (self.today_q_index or 0) >= 5)
        return {
            'id': self.id,
            'name': self.name or 'Nova',
            'appearance': self.get_appearance(),
            'hunger': self.hunger,
            'fitness': self.fitness,
            'happiness': self.happiness,
            'status': self.status,
            'care_tokens': self.care_tokens or 0,
            'days_alive': self.days_alive or 1,
            'total_correct': self.total_correct or 0,
            'quiz_done_today': quiz_done_today,
            'today_q_index': (self.today_q_index or 0) if self.last_quiz_date == today else 0,
            'today_correct': (self.today_correct or 0) if self.last_quiz_date == today else 0,
            'today_wrong': (self.today_wrong or 0) if self.last_quiz_date == today else 0,
            'sick_penalty_applied': bool(self.sick_penalty_applied),
        }
