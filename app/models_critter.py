"""Mondo Critters: daily trivia companion pet model.

Ultra-lightweight on the server: all 100+ animated character appearances are
stored as one ~120-byte JSON blob and rendered procedurally in SVG on the client.
"""
import json
from datetime import datetime

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

    # 4 core health stats (0..100). Keep all above 20 or neglect cascades!
    hunger = db.Column(db.Integer, default=80)
    fitness = db.Column(db.Integer, default=80)
    happiness = db.Column(db.Integer, default=80)
    education = db.Column(db.Integer, default=80)

    status = db.Column(db.String(20), default='healthy')  # healthy | warning | sick | fainted
    cascade_warning = db.Column(db.String(200), default='')
    care_tokens = db.Column(db.Integer, default=2)
    days_alive = db.Column(db.Integer, default=1)
    total_correct = db.Column(db.Integer, default=0)

    # Once-per-day care lock ('feed', 'exercise', 'play')
    care_used_date = db.Column(db.Date, nullable=True)
    care_used_json = db.Column(db.Text, default='[]')

    # Article reading & comprehension bonus tracking
    articles_read_json = db.Column(db.Text, default='[]')
    articles_quizzed_json = db.Column(db.Text, default='[]')

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

    def get_care_used_today(self) -> list:
        today = datetime.utcnow().date()
        if self.care_used_date != today:
            return []
        try:
            return list(json.loads(self.care_used_json or '[]'))
        except Exception:
            return []

    def mark_care_used_today(self, action: str):
        today = datetime.utcnow().date()
        cur = self.get_care_used_today()
        if action not in cur:
            cur.append(action)
        self.care_used_date = today
        self.care_used_json = json.dumps(cur)

    def get_articles_read(self) -> list:
        try:
            return list(json.loads(self.articles_read_json or '[]'))
        except Exception:
            return []

    def add_article_read(self, slug: str):
        cur = self.get_articles_read()
        if slug and slug not in cur:
            cur.append(slug)
            self.articles_read_json = json.dumps(cur[-200:])

    def get_articles_quizzed(self) -> list:
        try:
            return list(json.loads(self.articles_quizzed_json or '[]'))
        except Exception:
            return []

    def add_article_quizzed(self, slug: str):
        cur = self.get_articles_quizzed()
        if slug and slug not in cur:
            cur.append(slug)
            self.articles_quizzed_json = json.dumps(cur[-200:])

    def pending_article_bonuses(self) -> list:
        quizzed = set(self.get_articles_quizzed())
        return [s for s in self.get_articles_read() if s not in quizzed]

    def recalc_status(self):
        self.hunger = max(0, min(100, int(self.hunger if self.hunger is not None else 80)))
        self.fitness = max(0, min(100, int(self.fitness if self.fitness is not None else 80)))
        self.happiness = max(0, min(100, int(self.happiness if self.happiness is not None else 80)))
        self.education = max(0, min(100, int(self.education if self.education is not None else 80)))

        stats = {
            'Hunger': self.hunger,
            'Fitness': self.fitness,
            'Happiness': self.happiness,
            'Education': self.education,
        }
        low_bars = [k for k, v in stats.items() if v <= 20]
        if low_bars:
            self.cascade_warning = f"Low {' & '.join(low_bars)} will drain other bars if left neglected!"
        else:
            self.cascade_warning = ''

        lowest = min(stats.values())
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
        """Daily stat decay + cascading neglect penalty when any bar is <= 20."""
        today = datetime.utcnow().date()
        if not self.last_decay_date:
            self.last_decay_date = today
            return False
        delta = (today - self.last_decay_date).days
        if delta <= 0:
            return False
        if self.status != 'fainted':
            eff_days = min(delta, 4)
            base_drop = eff_days * 14

            # Check if any bar was already neglected (<= 20) — if so, cascade extra -10 to other bars!
            h = self.hunger if self.hunger is not None else 80
            f = self.fitness if self.fitness is not None else 80
            p = self.happiness if self.happiness is not None else 80
            e = self.education if self.education is not None else 80

            low_h, low_f, low_p, low_e = (h <= 20), (f <= 20), (p <= 20), (e <= 20)
            neglect_count = sum([low_h, low_f, low_p, low_e])
            cascade_extra = (10 * eff_days) if neglect_count > 0 else 0

            self.hunger = max(0, h - base_drop - (cascade_extra if not low_h else 0))
            self.fitness = max(0, f - base_drop - (cascade_extra if not low_f else 0))
            self.happiness = max(0, p - base_drop - (cascade_extra if not low_p else 0))
            self.education = max(0, e - (eff_days * 10) - (cascade_extra if not low_e else 0))

            self.days_alive = (self.days_alive or 1) + delta
        self.last_decay_date = today
        self.sick_penalty_applied = False
        self.recalc_status()
        return True

    def to_dict(self) -> dict:
        today = datetime.utcnow().date()
        quiz_done_today = bool(self.last_quiz_date == today and (self.today_q_index or 0) >= 5)
        pending = self.pending_article_bonuses()
        return {
            'id': self.id,
            'name': self.name or 'Nova',
            'appearance': self.get_appearance(),
            'hunger': self.hunger if self.hunger is not None else 80,
            'fitness': self.fitness if self.fitness is not None else 80,
            'happiness': self.happiness if self.happiness is not None else 80,
            'education': self.education if self.education is not None else 80,
            'status': self.status,
            'cascade_warning': self.cascade_warning or '',
            'care_tokens': self.care_tokens or 0,
            'care_used_today': self.get_care_used_today(),
            'days_alive': self.days_alive or 1,
            'total_correct': self.total_correct or 0,
            'quiz_done_today': quiz_done_today,
            'today_q_index': (self.today_q_index or 0) if self.last_quiz_date == today else 0,
            'today_correct': (self.today_correct or 0) if self.last_quiz_date == today else 0,
            'today_wrong': (self.today_wrong or 0) if self.last_quiz_date == today else 0,
            'sick_penalty_applied': bool(self.sick_penalty_applied),
            'articles_read_count': len(self.get_articles_read()),
            'pending_article_bonuses': pending,
        }
