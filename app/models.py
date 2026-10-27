import json
import re
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


def slugify(text: str) -> str:
    """Convert text into URL-friendly slug."""
    text = (text or '').strip().lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-') or 'item'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')  # admin, editor, author
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, default='')

    posts = db.relationship('Post', backref='category', lazy='dynamic')


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, default='')
    excerpt = db.Column(db.Text, default='')
    featured_image = db.Column(db.String(300), default='')
    status = db.Column(db.String(20), default='publish')  # 'publish', 'draft'
    is_pinned = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    modules = db.relationship('PageModule', backref='post', cascade='all, delete-orphan', lazy='dynamic')

    # SEO & Social Graph Meta Fields
    meta_title = db.Column(db.String(255), default='')
    meta_description = db.Column(db.Text, default='')
    meta_keywords = db.Column(db.String(255), default='')
    canonical_url = db.Column(db.String(500), default='')
    og_image = db.Column(db.String(500), default='')
    no_index = db.Column(db.Boolean, default=False)


class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, default='')
    excerpt = db.Column(db.Text, default='')
    template = db.Column(db.String(50), default='default')  # default, full-width, contact
    status = db.Column(db.String(20), default='publish')  # publish, draft
    sort_order = db.Column(db.Integer, default=0)
    show_in_nav = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    modules = db.relationship('PageModule', backref='page', cascade='all, delete-orphan', lazy='dynamic')

    # SEO & Social Graph Meta Fields
    meta_title = db.Column(db.String(255), default='')
    meta_description = db.Column(db.Text, default='')
    meta_keywords = db.Column(db.String(255), default='')
    canonical_url = db.Column(db.String(500), default='')
    og_image = db.Column(db.String(500), default='')
    no_index = db.Column(db.Boolean, default=False)


class PageModule(db.Model):
    __tablename__ = 'page_modules'

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=True, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True, index=True)
    is_home = db.Column(db.Boolean, default=False, index=True)
    theme = db.Column(db.String(50), default='quizhub', index=True)

    module_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), default='')
    placement = db.Column(db.String(20), default='above')  # 'above' or 'below' content
    sort_order = db.Column(db.Integer, default=0)
    is_enabled = db.Column(db.Boolean, default=True)

    config_json = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_config(self) -> dict:
        if not self.config_json:
            return {}
        try:
            return json.loads(self.config_json)
        except Exception:
            return {}

    def set_config(self, cfg: dict):
        self.config_json = json.dumps(cfg or {})


class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(100), default='image/jpeg')
    file_size = db.Column(db.Integer, default=0)
    alt_text = db.Column(db.String(255), default='')
    caption = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(30), default='header')  # header, footer
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    open_new_tab = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=True)

    children = db.relationship(
        'MenuItem',
        backref=db.backref('parent', remote_side=[id]),
        cascade='all, delete-orphan',
        lazy='joined',
        order_by='MenuItem.sort_order.asc()'
    )


class SidebarWidget(db.Model):
    __tablename__ = 'sidebar_widgets'

    id = db.Column(db.Integer, primary_key=True)
    sidebar_id = db.Column(db.String(50), default='sidebar-right')  # sidebar-left, sidebar-right, footer-1, footer-2
    widget_type = db.Column(db.String(50), nullable=False)  # recent_posts, custom_html, categories, image, search, contact_card
    title = db.Column(db.String(120), default='')
    content = db.Column(db.Text, default='')
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    config_json = db.Column(db.Text, default='{}')

    def get_config(self) -> dict:
        if not self.config_json:
            return {}
        try:
            return json.loads(self.config_json)
        except Exception:
            return {}

    def set_config(self, cfg: dict):
        self.config_json = json.dumps(cfg or {})


class SiteSetting(db.Model):
    __tablename__ = 'site_settings'

    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Text, default='')

    @classmethod
    def get(cls, key: str, default=None):
        item = cls.query.filter_by(key=key).first()
        if item is None:
            return default
        return item.value

    @classmethod
    def set(cls, key: str, value: str):
        item = cls.query.filter_by(key=key).first()
        if not item:
            item = cls(key=key, value=value)
            db.session.add(item)
        else:
            item.value = value
        db.session.commit()

    @classmethod
    def get_all(cls) -> dict:
        items = cls.query.all()
        return {item.key: item.value for item in items}


# ==============================================================================
# QUIZMONDO ARENA GAMIFICATION & MULTIPLAYER MODELS
# ==============================================================================

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(30), default='classic')  # classic, audio, image, video, shape_click, slider
    media_url = db.Column(db.String(500), default='')
    options_json = db.Column(db.Text, default='{}')  # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_option = db.Column(db.String(50), nullable=False)  # 'A', 'B', 'C', 'D'
    explanation = db.Column(db.Text, default='')
    category_slug = db.Column(db.String(80), index=True, default='general')
    category_name = db.Column(db.String(100), default='General Knowledge')
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    points = db.Column(db.Integer, default=100)
    time_limit = db.Column(db.Integer, default=15)
    pack_slug = db.Column(db.String(80), index=True, default='core')
    is_community = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='approved')  # approved, pending, rejected
    author_name = db.Column(db.String(80), default='Quizmondo Master')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_options(self) -> dict:
        try:
            return json.loads(self.options_json or '{}')
        except Exception:
            return {}

    def set_options(self, opts: dict):
        self.options_json = json.dumps(opts or {})

    def to_dict(self, include_answer=False) -> dict:
        data = {
            'id': self.id,
            'prompt': self.prompt,
            'question_type': self.question_type,
            'media_url': self.media_url,
            'options': self.get_options(),
            'category_slug': self.category_slug,
            'category_name': self.category_name,
            'difficulty': self.difficulty,
            'points': self.points,
            'time_limit': self.time_limit,
            'author_name': self.author_name,
            'is_community': self.is_community,
            'status': self.status
        }
        if include_answer:
            data['correct_option'] = self.correct_option
            data['explanation'] = self.explanation
        return data


class PlayerProfile(db.Model):
    __tablename__ = 'player_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    session_key = db.Column(db.String(64), unique=True, index=True, nullable=False)
    display_name = db.Column(db.String(80), nullable=False, default='Player')
    avatar_key = db.Column(db.String(40), default='quizzy')  # quizzy, nova, pixel, sage, cyber_fox, brain_bot
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=250)
    streak_days = db.Column(db.Integer, default=1)
    matches_played = db.Column(db.Integer, default=0)
    matches_won = db.Column(db.Integer, default=0)
    is_banned = db.Column(db.Boolean, default=False)
    ban_reason = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active_at = db.Column(db.DateTime, default=datetime.utcnow)

    def add_xp(self, amount: int):
        self.xp = (self.xp or 0) + max(0, amount)
        # 500 XP per level
        self.level = 1 + (self.xp // 500)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'session_key': self.session_key,
            'display_name': self.display_name,
            'avatar_key': self.avatar_key,
            'level': self.level,
            'xp': self.xp,
            'coins': self.coins,
            'streak_days': self.streak_days,
            'matches_played': self.matches_played,
            'matches_won': self.matches_won,
            'win_rate': round((self.matches_won / self.matches_played * 100), 1) if self.matches_played > 0 else 0
        }


class ArenaMatch(db.Model):
    __tablename__ = 'arena_matches'

    id = db.Column(db.Integer, primary_key=True)
    match_code = db.Column(db.String(32), unique=True, index=True, nullable=False)
    player1_session = db.Column(db.String(64), nullable=False, index=True)
    player1_name = db.Column(db.String(80), default='Player 1')
    player1_avatar = db.Column(db.String(40), default='quizzy')
    player2_session = db.Column(db.String(64), nullable=True, index=True)
    player2_name = db.Column(db.String(80), default='Awaiting Challenger...')
    player2_avatar = db.Column(db.String(40), default='nova')
    status = db.Column(db.String(20), default='waiting')  # waiting, in_progress, completed, forfeited
    current_round = db.Column(db.Integer, default=1)  # 1 to 6
    current_turn = db.Column(db.Integer, default=1)  # 1 (player1) or 2 (player2)
    winner = db.Column(db.Integer, default=0)  # 0: ongoing/tie, 1: player1, 2: player2
    p1_total_score = db.Column(db.Integer, default=0)
    p2_total_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    rounds = db.relationship('ArenaRound', backref='match', cascade='all, delete-orphan', lazy='dynamic', order_by='ArenaRound.round_number.asc()')

    @property
    def is_bot(self) -> bool:
        return self.player2_session == 'bot_quizmondo_ai' or bool(self.player2_name and 'bot' in self.player2_name.lower())

    def expected_turn(self) -> int:
        """Deterministic Snake Turn Order:
        - Whoever caught up to finish the previous round leads the next one, which
          is the player recorded in the round's chosen_by when the round was created.
        - Once one player has answered, the other one is up.
        """
        if self.is_bot:
            return 1
        active_round = self.rounds.filter_by(round_number=self.current_round).first()
        if not active_round:
            return 1
        p1_done = bool(active_round.p1_answers_json and active_round.p1_answers_json != '[]')
        p2_done = bool(active_round.p2_answers_json and active_round.p2_answers_json != '[]')
        if p1_done and not p2_done:
            return 2
        if p2_done and not p1_done:
            return 1
        # Nobody has played this round yet: the player who leads it off is the one
        # submit_round recorded as chosen_by. Falling back to round parity here is
        # what used to disagree with submit_round whenever Player 2 led Round 1.
        if active_round.chosen_by in (1, 2):
            return active_round.chosen_by
        return 1 if (self.current_round % 2 == 1) else 2

    def is_player_turn(self, session_key: str) -> bool:
        if self.status != 'in_progress' and self.status != 'waiting':
            return False
        # If playing against an AI bot, it is ALWAYS the human player's turn to play
        if self.is_bot:
            return self.player1_session == session_key
        exp_turn = self.expected_turn()
        if self.player1_session == session_key:
            return exp_turn == 1
        if self.player2_session == session_key:
            return exp_turn == 2
        return False

    def to_dict(self) -> dict:
        return {
            'match_code': self.match_code,
            'player1_name': self.player1_name,
            'player1_avatar': self.player1_avatar,
            'player2_name': self.player2_name,
            'player2_avatar': self.player2_avatar,
            'status': self.status,
            'current_round': self.current_round,
            'current_turn': self.current_turn,
            'winner': self.winner,
            'p1_total_score': self.p1_total_score,
            'p2_total_score': self.p2_total_score,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }


class ArenaRound(db.Model):
    __tablename__ = 'arena_rounds'

    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('arena_matches.id', ondelete='CASCADE'), nullable=False, index=True)
    round_number = db.Column(db.Integer, nullable=False)  # 1 to 6
    category_slug = db.Column(db.String(80), default='general')
    category_name = db.Column(db.String(100), default='General Knowledge')
    chosen_by = db.Column(db.Integer, default=1)  # 1 or 2
    question_ids_json = db.Column(db.Text, default='[]')
    p1_score = db.Column(db.Integer, default=0)
    p1_answers_json = db.Column(db.Text, default='[]')
    p2_score = db.Column(db.Integer, default=0)
    p2_answers_json = db.Column(db.Text, default='[]')
    status = db.Column(db.String(20), default='pending')  # pending, p1_done, p2_done, completed

    def get_question_ids(self) -> list:
        try:
            return json.loads(self.question_ids_json or '[]')
        except Exception:
            return []

    def set_question_ids(self, q_ids: list):
        self.question_ids_json = json.dumps(q_ids or [])

    def get_p1_answers(self) -> list:
        try:
            return json.loads(self.p1_answers_json or '[]')
        except Exception:
            return []

    def get_p2_answers(self) -> list:
        try:
            return json.loads(self.p2_answers_json or '[]')
        except Exception:
            return []

    def get_p1_summary(self) -> dict:
        ans = self.get_p1_answers()
        done = bool(ans)
        correct_count = sum(1 for a in ans if a.get('is_correct'))
        total_time = round(sum(float(a.get('time_taken', max(0, 15 - float(a.get('time_left', 10))))) for a in ans), 1) if done else 0.0
        return {
            'done': done,
            'score': self.p1_score or 0,
            'correct_count': correct_count,
            'total_questions': len(ans) or 3,
            'total_time_sec': total_time
        }

    def get_p2_summary(self) -> dict:
        ans = self.get_p2_answers()
        done = bool(ans)
        correct_count = sum(1 for a in ans if a.get('is_correct'))
        total_time = round(sum(float(a.get('time_taken', max(0, 15 - float(a.get('time_left', 10))))) for a in ans), 1) if done else 0.0
        return {
            'done': done,
            'score': self.p2_score or 0,
            'correct_count': correct_count,
            'total_questions': len(ans) or 3,
            'total_time_sec': total_time
        }


class QuizPack(db.Model):
    __tablename__ = 'quiz_packs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, index=True, nullable=False)
    description = db.Column(db.Text, default='')
    icon = db.Column(db.String(50), default='🎮')
    category_slug = db.Column(db.String(80), default='general')
    is_community = db.Column(db.Boolean, default=False)
    author_name = db.Column(db.String(80), default='Quizmondo Team')
    question_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PubLeague(db.Model):
    __tablename__ = 'pub_leagues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, index=True, nullable=False)
    pin_code = db.Column(db.String(10), default='1234')
    venue_name = db.Column(db.String(150), default='Virtual Pub Quiz Arena')
    description = db.Column(db.Text, default='')
    schedule_day = db.Column(db.String(50), default='Every Thursday 20:00')
    is_active = db.Column(db.Boolean, default=True)
    teams_json = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_virtual_league(self) -> bool:
        s = (self.slug or '').lower()
        n = (self.name or '').lower()
        v = (self.venue_name or '').lower()
        return 'online' in s or 'cyber' in s or 'virtual' in n or 'virtual' in v

    def get_state(self) -> dict:
        default_config = {
            'total_rounds': 3 if self.is_virtual_league() else 5,
            'max_tables': 20,
            'question_time_limit': 15,
            'interval_duration_mins': 8,
            'bar_promo_enabled': True,
            'promo_title': 'Half-Time Bar Special: 10% Off All Drinks!',
            'promo_desc': 'Show this screen at the main bar during the interval for 10% off all draught pints, wine & bar snacks.',
            'promo_code': 'ROUND2SPECIAL',
            'first_prize': '£20 Bar Tab Voucher + Golden Trophy',
            'second_prize': 'Free Bottle of House Wine for the Table'
        }
        try:
            data = json.loads(self.teams_json or '{}')
            if isinstance(data, dict):
                data.setdefault('teams', [])
                data.setdefault('current_round', 1)
                data.setdefault('round_status', 'waiting')
                data.setdefault('answers_revealed', False)
                data.setdefault('config', default_config)
                # Ensure all subkeys in config exist
                for k, v in default_config.items():
                    data['config'].setdefault(k, v)
                return data
            elif isinstance(data, list):
                return {
                    'teams': data,
                    'current_round': 1,
                    'round_status': 'waiting',
                    'answers_revealed': False,
                    'config': default_config
                }
        except Exception:
            pass
        return {
            'teams': [],
            'current_round': 1,
            'round_status': 'waiting',
            'answers_revealed': False,
            'config': default_config
        }

    def set_state(self, state: dict):
        self.teams_json = json.dumps(state)

    def get_teams(self) -> list:
        return self.get_state().get('teams', [])

    def set_teams(self, teams: list):
        state = self.get_state()
        state['teams'] = teams
        self.set_state(state)
