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

    # 5 core health stats (0..100). Education starts at 30 so neglecting reading soon cascades!
    hunger = db.Column(db.Integer, default=80)
    fitness = db.Column(db.Integer, default=80)
    happiness = db.Column(db.Integer, default=80)
    education = db.Column(db.Integer, default=30)
    attention = db.Column(db.Integer, default=75)

    status = db.Column(db.String(20), default='healthy')  # healthy | warning | sick | fainted
    cascade_warning = db.Column(db.String(200), default='')
    care_tokens = db.Column(db.Integer, default=2)
    days_alive = db.Column(db.Integer, default=1)
    total_correct = db.Column(db.Integer, default=0)

    # Once-per-day care lock ('feed', 'exercise', 'play')
    care_used_date = db.Column(db.Date, nullable=True)
    care_used_json = db.Column(db.Text, default='[]')

    # Study bonus cap: max 3 per UTC day (+5 Education each)
    study_bonus_date = db.Column(db.Date, nullable=True)
    study_bonus_count = db.Column(db.Integer, default=0)

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
            merged.update({k: v for k, v in data.items() if v is not None and not str(k).startswith('_')})
            return merged
        except Exception:
            return dict(DEFAULT_APPEARANCE)

    def set_appearance(self, data: dict):
        raw = {}
        try:
            raw = json.loads(self.appearance_json or '{}')
        except Exception:
            raw = {}
        cur = self.get_appearance()
        for k in ('species', 'preset_id', 'color', 'accent', 'hair', 'hat', 'scarf'):
            if k in data:
                cur[k] = data[k]
        # Preserve internal decay tick timestamps stored in appearance_json
        for meta_k in ('_decay_ts', '_edu_tick'):
            if meta_k in raw:
                cur[meta_k] = raw[meta_k]
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

    def get_study_bonuses_today(self) -> int:
        today = datetime.utcnow().date()
        if self.study_bonus_date != today:
            return 0
        return int(self.study_bonus_count or 0)

    def increment_study_bonus_today(self):
        today = datetime.utcnow().date()
        if self.study_bonus_date != today:
            self.study_bonus_date = today
            self.study_bonus_count = 1
        else:
            self.study_bonus_count = int(self.study_bonus_count or 0) + 1

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
        self.education = max(0, min(100, int(self.education if self.education is not None else 30)))
        self.attention = max(0, min(100, int(self.attention if self.attention is not None else 75)))

        stats = {
            'Hunger': self.hunger,
            'Fitness': self.fitness,
            'Happiness': self.happiness,
            'Education': self.education,
            'Attention': self.attention,
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

    @staticmethod
    def _tiered_tick_loss(val: int, tick_num: int) -> int:
        """Tiered stat loss per tick:
        - < 30: loses 3 points
        - < 60: loses 2 points
        - < 90: loses 1 point
        - >= 90: loses 1 point every 2nd tick (grace buffer so 90-100 still gently drifts below 90)
        """
        if val < 30:
            return 3
        if val < 60:
            return 2
        if val < 90:
            return 1
        return 1 if (tick_num % 2 == 0) else 0

    def reset_decay_clock(self):
        """Reset the 3-hour tiered decay clock (called on creation or fresh hatch)."""
        try:
            raw = json.loads(self.appearance_json or '{}')
        except Exception:
            raw = dict(DEFAULT_APPEARANCE)
        raw['_decay_ts'] = int(datetime.utcnow().timestamp())
        raw['_edu_tick'] = 0
        self.appearance_json = json.dumps(raw)
        self.last_decay_date = datetime.utcnow().date()

    def apply_daily_decay(self):
        """Tiered 3-hour stat decay (<90: -1, <60: -2, <30: -3) + half-speed Education decay (every 6h)
        + cascading neglect penalty when any bar is <= 20.
        """
        now_utc = datetime.utcnow()
        today = now_utc.date()
        now_ts = int(now_utc.timestamp())
        changed = False

        # Calendar-day survival counter & daily sickness reset
        if not self.last_decay_date:
            self.last_decay_date = today
            changed = True
        else:
            day_delta = (today - self.last_decay_date).days
            if day_delta > 0:
                if self.status != 'fainted':
                    self.days_alive = (self.days_alive or 1) + day_delta
                self.last_decay_date = today
                self.sick_penalty_applied = False
                changed = True

        try:
            raw = json.loads(self.appearance_json or '{}')
        except Exception:
            raw = dict(DEFAULT_APPEARANCE)

        last_ts = raw.get('_decay_ts')
        edu_tick = int(raw.get('_edu_tick') or 0)
        if not isinstance(last_ts, (int, float)) or last_ts <= 0:
            raw['_decay_ts'] = now_ts
            raw['_edu_tick'] = edu_tick
            self.appearance_json = json.dumps(raw)
            if changed:
                self.recalc_status()
            return True

        # 1 tick = 3 hours (10,800 seconds). Education ticks at half speed (every 2nd tick = 6 hours).
        TICK_SECONDS = 10800
        elapsed_ticks = int((now_ts - int(last_ts)) // TICK_SECONDS)
        if elapsed_ticks <= 0:
            if changed:
                self.recalc_status()
            return changed

        if self.status != 'fainted':
            eff_ticks = min(elapsed_ticks, 24)  # Cap catch-up at 72 hours (24 ticks)
            h = self.hunger if self.hunger is not None else 80
            f = self.fitness if self.fitness is not None else 80
            p = self.happiness if self.happiness is not None else 80
            e = self.education if self.education is not None else 30
            a = self.attention if self.attention is not None else 75

            for _ in range(eff_ticks):
                edu_tick = (edu_tick + 1) % 2
                low_h, low_f, low_p, low_e, low_a = (h <= 20), (f <= 20), (p <= 20), (e <= 20), (a <= 20)
                has_neglect = any((low_h, low_f, low_p, low_e, low_a))

                h = max(0, h - self._tiered_tick_loss(h, edu_tick) - (1 if (has_neglect and not low_h) else 0))
                f = max(0, f - self._tiered_tick_loss(f, edu_tick) - (1 if (has_neglect and not low_f) else 0))
                p = max(0, p - self._tiered_tick_loss(p, edu_tick) - (1 if (has_neglect and not low_p) else 0))
                a = max(0, a - self._tiered_tick_loss(a, edu_tick) - (1 if (has_neglect and not low_a) else 0))

                # Education decays at HALF speed (every 6 hours = every 2nd 3-hour tick)
                if edu_tick == 0:
                    e = max(0, e - self._tiered_tick_loss(e, 0) - (1 if (has_neglect and not low_e) else 0))

                if min(h, f, p, e, a) <= 0:
                    break

            self.hunger, self.fitness, self.happiness, self.education, self.attention = h, f, p, e, a

        raw['_decay_ts'] = int(last_ts) + (elapsed_ticks * TICK_SECONDS)
        raw['_edu_tick'] = edu_tick
        self.appearance_json = json.dumps(raw)
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
            'education': self.education if self.education is not None else 30,
            'attention': self.attention if self.attention is not None else 75,
            'status': self.status,
            'cascade_warning': self.cascade_warning or '',
            'care_tokens': self.care_tokens or 0,
            'care_used_today': self.get_care_used_today(),
            'study_bonuses_today': self.get_study_bonuses_today(),
            'study_bonus_limit': 3,
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
