import json
import re
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Minimum age to hold an account, unless admin says otherwise. The Data
# Protection Act 2018 sets 13 as the age of consent for an information society
# service in the UK, so that is the default and the sensible floor.
MINIMUM_SIGNUP_AGE = 13


def age_gate_config():
    """Whether signup asks for an age, and what the minimum is.

    Both are set in Settings > Security. The gate is on unless it has been
    turned off deliberately, so a fresh install is never accidentally open.
    """
    enabled = (SiteSetting.get('age_gate_enabled', '1') or '') != ''
    try:
        minimum = int(SiteSetting.get('minimum_signup_age', '') or MINIMUM_SIGNUP_AGE)
    except (TypeError, ValueError):
        minimum = MINIMUM_SIGNUP_AGE
    return {'enabled': enabled, 'minimum': max(0, min(21, minimum))}


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

    # Age. Under the Data Protection Act 2018 a child in the UK can consent to an
    # online service at 13, so that is the floor for signing up here. The date of
    # birth is kept rather than a bare tickbox, because a tickbox tells you
    # nothing later and the date is what any check has to be made against.
    date_of_birth = db.Column(db.Date, nullable=True)
    age_confirmed_at = db.Column(db.DateTime, nullable=True)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def age_years(self, on=None):
        """Age in whole years, or None if no date of birth was given."""
        if not self.date_of_birth:
            return None
        on = on or datetime.utcnow().date()
        born = self.date_of_birth
        return on.year - born.year - ((on.month, on.day) < (born.month, born.day))

    def is_minor(self) -> bool:
        """Under 18, so advertising stays non-personalised and nothing is profiled."""
        age = self.age_years()
        return age is None or age < 18

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
    # Lower sorts first among pinned posts, so the how-to guides can be put in reading order
    pin_order = db.Column(db.Integer, default=0)
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


class GroupGame(db.Model):
    """A live group quiz: several players answering the same question at the same time.

    Deliberately separate from ArenaMatch, which is hard-wired to two players through
    its player1_/player2_ columns and cannot hold six. The timing model is borrowed from
    the pub league instead: a deadline per question, applied whenever anybody polls, so
    the game runs itself without a host.
    """
    __tablename__ = 'group_games'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(12), unique=True, index=True, nullable=False)
    # lobby -> active -> reveal -> (active ...) -> finished
    status = db.Column(db.String(20), default='lobby', index=True)
    category_slug = db.Column(db.String(80), default='')
    category_name = db.Column(db.String(120), default='')

    min_players = db.Column(db.Integer, default=3)
    max_players = db.Column(db.Integer, default=6)
    total_questions = db.Column(db.Integer, default=8)
    seconds_per_question = db.Column(db.Integer, default=15)
    reveal_seconds = db.Column(db.Integer, default=4)

    question_ids_json = db.Column(db.Text, default='[]')
    current_index = db.Column(db.Integer, default=0)
    # Set once the minimum is met: the lobby countdown everyone can see
    starts_at = db.Column(db.DateTime, nullable=True)
    question_ends_at = db.Column(db.DateTime, nullable=True)
    reveal_ends_at = db.Column(db.DateTime, nullable=True)

    host_key = db.Column(db.String(120), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def get_question_ids(self) -> list:
        try:
            return json.loads(self.question_ids_json or '[]')
        except Exception:
            return []

    def set_question_ids(self, ids):
        self.question_ids_json = json.dumps(list(ids or []))

    def humans(self):
        return [p for p in self.players if not p.is_bot]

    def is_full(self) -> bool:
        return self.players.count() >= (self.max_players or 6)


class GroupPlayer(db.Model):
    """A seat in a group game.

    Bots live here and nowhere else: no PlayerProfile row, no session key, no XP. Because
    nothing outside a group game reads this table, a bot cannot turn up on the leaderboard,
    in a friends roster or in the open challenge list. It stops existing with the game.
    """
    __tablename__ = 'group_players'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('group_games.id'), index=True, nullable=False)
    # Null for a bot; otherwise the PlayerProfile session key
    player_key = db.Column(db.String(120), index=True, default=None)
    display_name = db.Column(db.String(80), default='Player')
    avatar_key = db.Column(db.String(40), default='quizzy')
    is_bot = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    answers_json = db.Column(db.Text, default='{}')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    game = db.relationship('GroupGame', backref=db.backref('players', lazy='dynamic', cascade='all, delete-orphan'))

    def get_answers(self) -> dict:
        try:
            return json.loads(self.answers_json or '{}')
        except Exception:
            return {}

    def set_answers(self, data):
        self.answers_json = json.dumps(data or {})

    def answer_for(self, index):
        return self.get_answers().get(str(index))


class FeaturedGame(db.Model):
    """A slide in the hero's featured game gallery.

    The hero used to hard-code one image and one caption, so changing what the
    homepage promoted meant editing a template. These are rows instead: add a few,
    order them, and the hero rotates through whatever is active.
    """
    __tablename__ = 'featured_games'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(60), default='FEATURED GAME')
    title = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(500), default='')
    link_url = db.Column(db.String(500), default='/arena/')
    cta_text = db.Column(db.String(40), default='PLAY NOW')
    # Optional: ties the slide to a quiz category, purely for the admin's own reference
    category_slug = db.Column(db.String(80), default='')
    credit = db.Column(db.String(200), default='')
    # Optional YouTube background, played silently behind the slide. The image stays
    # as the poster while it loads and as the fallback where video will not play.
    video_url = db.Column(db.String(500), default='')
    # Optional clip, in seconds. 0 for either means "from the top" / "to the end",
    # so an advertiser can show the ten seconds that matter rather than a whole film.
    video_start = db.Column(db.Integer, default=0)
    video_end = db.Column(db.Integer, default=0)
    sort_order = db.Column(db.Integer, default=0, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def youtube_id(self) -> str:
        """The video id out of whatever YouTube URL was pasted in."""
        src = (self.video_url or '').strip()
        if not src:
            return ''
        patterns = (
            r'(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{6,20})',
            r'(?:youtu\.be/)([A-Za-z0-9_-]{6,20})',
            r'(?:youtube\.com/embed/)([A-Za-z0-9_-]{6,20})',
            r'(?:youtube\.com/shorts/)([A-Za-z0-9_-]{6,20})',
        )
        for pattern in patterns:
            found = re.search(pattern, src)
            if found:
                return found.group(1)
        # A bare id pasted on its own
        if re.fullmatch(r'[A-Za-z0-9_-]{6,20}', src):
            return src
        return ''

    def youtube_embed_url(self) -> str:
        """The background player URL, clipped if a start or end was given.

        Served from youtube-nocookie.com, muted, looping, with controls, branding
        and keyboard off so it behaves as a background rather than a player.
        """
        vid = self.youtube_id()
        if not vid:
            return ''
        start = max(0, int(self.video_start or 0))
        end = max(0, int(self.video_end or 0))
        params = [
            'autoplay=1', 'mute=1', 'loop=1', 'playlist=' + vid,
            'controls=0', 'showinfo=0', 'rel=0', 'modestbranding=1',
            'playsinline=1', 'disablekb=1', 'iv_load_policy=3',
        ]
        if start:
            params.append('start=%d' % start)
        if end > start:
            params.append('end=%d' % end)
        return 'https://www.youtube-nocookie.com/embed/%s?%s' % (vid, '&'.join(params))

    def clip_label(self) -> str:
        """How the clip reads in the admin list."""
        start = int(self.video_start or 0)
        end = int(self.video_end or 0)

        def mmss(total):
            return '%d:%02d' % (total // 60, total % 60)

        if start and end > start:
            return '%s to %s' % (mmss(start), mmss(end))
        if start:
            return 'from %s' % mmss(start)
        if end:
            return 'first %s' % mmss(end)
        return 'whole video'

    def resolved_image(self) -> str:
        """Where the image actually lives: an uploaded file, a pasted URL, or the packaged fallback."""
        src = (self.image_url or '').strip()
        if not src:
            return '/static/img/quizhub_hero.jpg'
        if src.startswith(('http://', 'https://', '/')):
            return src
        return '/static/img/' + src


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
    last_wheel_spin_at = db.Column(db.DateTime, nullable=True)
    climber_shields = db.Column(db.Integer, default=0)
    is_banned = db.Column(db.Boolean, default=False)
    ban_reason = db.Column(db.String(255), default='')
    # Paused by the player: hidden from public lists, and reversible by signing in
    is_paused = db.Column(db.Boolean, default=False, index=True)
    # Erased by the player: the identity is gone for good and only the score remains.
    # There is deliberately no way back from this, which is what makes it erasure
    # under Article 17 rather than pseudonymisation.
    is_anonymised = db.Column(db.Boolean, default=False, index=True)
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
            'win_rate': round((self.matches_won / self.matches_played * 100), 1) if self.matches_played > 0 else 0,
            'last_wheel_spin_at': self.last_wheel_spin_at.isoformat() if self.last_wheel_spin_at else None,
            'climber_shields': self.climber_shields if self.climber_shields is not None else 0
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
    is_virtual = db.Column(db.Boolean, default=False)
    teams_json = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def looks_virtual(self) -> bool:
        """Guess the mode from the slug, used to seed the flag and as a legacy fallback.

        Only the slug counts. A physical pub can easily call its night a 'Virtual
        Pub Showdown' in the league name or the venue name, and reading those is
        what had The Red Lion running as an online league.
        """
        s = (self.slug or '').lower()
        return 'online' in s or 'cyber' in s or 'virtual' in s

    def is_virtual_league(self) -> bool:
        # The explicit admin toggle wins; leagues from before the column fall back to the naming
        if self.is_virtual is None:
            return self.looks_virtual()
        return bool(self.is_virtual)

    def get_state(self) -> dict:
        virtual = self.is_virtual_league()
        default_config = {
            'total_rounds': 3 if virtual else 5,
            'max_tables': 20,
            'question_time_limit': 15,
            'interval_duration_mins': 8,
            # Lock a round by itself once the clock has run out for every table
            'round_deadline_enabled': True,
            # A virtual league has no host in the room, so it rolls on to the next round by itself
            'auto_advance_enabled': virtual,
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


def pub_season_label(when=None) -> str:
    """The season a quiz night belongs to.

    A pub quiz season runs with the football year rather than the calendar
    one, so an autumn night and the following spring stay in the same table.
    """
    when = when or datetime.utcnow()
    start = when.year if when.month >= 8 else when.year - 1
    return f"{start}/{str(start + 1)[-2:]}"


class PubLeagueResult(db.Model):
    """One team's finishing position on one quiz night.

    The league itself only holds the night in progress, and a reset wipes it,
    so a finalised tournament is copied in here. This is the only record of
    what happened, and everything the league tables show is built from it.
    """
    __tablename__ = 'pub_league_results'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey('pub_leagues.id'), index=True, nullable=False)
    season = db.Column(db.String(20), index=True, default='')
    played_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    team_name = db.Column(db.String(150), nullable=False)
    # Normalised name, so a team is still itself when someone retypes it
    team_key = db.Column(db.String(150), index=True, default='')
    table_num = db.Column(db.String(20), default='')
    position = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    rounds_played = db.Column(db.Integer, default=0)
    round_scores_json = db.Column(db.Text, default='{}')
    members = db.Column(db.Integer, default=1)

    league = db.relationship('PubLeague', backref=db.backref('results', lazy='dynamic'))

    def get_round_scores(self) -> dict:
        try:
            return json.loads(self.round_scores_json or '{}')
        except Exception:
            return {}

    def league_points(self) -> int:
        """Table points for the night: 3 for a win, 2 for second, 1 for third, 1 for turning up."""
        return {1: 3, 2: 2, 3: 1}.get(self.position, 1)


# ======================================================================
# Advertising
#
# Ads are entered by an admin, never by the advertiser, so nothing reaches a
# page without somebody here having looked at it. Three kinds fill a slot, in
# this order of preference: a direct-sold ad that somebody is paying for, then
# an AdSense unit filling what is unsold, then a house ad for Quizmondo's own
# games rather than a hole in the layout.
#
# The site is for all ages, so every ad carries a family-safety decision and
# nothing runs until that decision is a yes.
# ======================================================================

AD_SLOTS = [
    ('hero', 'Hero carousel (rotates with the featured games)'),
    ('sidebar', 'Sidebar (right column)'),
    ('leaderboard', 'Leaderboard (wide banner, top of page)'),
    ('in_feed', 'In feed (between article or quiz cards)'),
    ('interstitial', 'Between rounds (pub quiz and duel breaks)'),
]

AD_KINDS = [
    ('image', 'Image banner'),
    ('youtube', 'YouTube video'),
    ('adsense', 'Google AdSense unit'),
    ('house', 'House ad (our own games)'),
]


class Advertisement(db.Model):
    __tablename__ = 'advertisements'

    id = db.Column(db.Integer, primary_key=True)

    # What it is, and who it is for
    name = db.Column(db.String(150), nullable=False)          # internal label
    advertiser = db.Column(db.String(150), default='')
    advertiser_email = db.Column(db.String(200), default='')
    notes = db.Column(db.Text, default='')                    # rate agreed, invoice ref

    kind = db.Column(db.String(20), default='image', index=True)
    slot = db.Column(db.String(30), default='sidebar', index=True)

    # Creative
    image_url = db.Column(db.String(500), default='')
    link_url = db.Column(db.String(500), default='')
    headline = db.Column(db.String(150), default='')
    body_text = db.Column(db.String(300), default='')
    alt_text = db.Column(db.String(200), default='')
    video_url = db.Column(db.String(500), default='')
    video_start = db.Column(db.Integer, default=0)
    video_end = db.Column(db.Integer, default=0)
    video_title = db.Column(db.String(300), default='')       # fetched from YouTube, for the safety check
    adsense_slot_id = db.Column(db.String(60), default='')

    # When it runs. Null either side means open-ended.
    starts_at = db.Column(db.DateTime, nullable=True)
    ends_at = db.Column(db.DateTime, nullable=True)
    weight = db.Column(db.Integer, default=10)                # rotation share within a slot
    is_active = db.Column(db.Boolean, default=True, index=True)

    # Family-safety. approved_family is the human decision and the thing that
    # actually gates serving; safety_notes is what the automated check found.
    approved_family = db.Column(db.Boolean, default=False, index=True)
    safety_notes = db.Column(db.Text, default='')
    reviewed_by = db.Column(db.String(80), default='')
    reviewed_at = db.Column(db.DateTime, nullable=True)

    # Running totals. The per-day detail lives in AdStat.
    impressions = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def youtube_id(self) -> str:
        """The video id out of whatever YouTube URL was pasted in."""
        src = (self.video_url or '').strip()
        if not src:
            return ''
        patterns = (
            r'(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{6,20})',
            r'(?:youtu\.be/)([A-Za-z0-9_-]{6,20})',
            r'(?:youtube\.com/embed/)([A-Za-z0-9_-]{6,20})',
            r'(?:youtube\.com/shorts/)([A-Za-z0-9_-]{6,20})',
        )
        for pattern in patterns:
            found = re.search(pattern, src)
            if found:
                return found.group(1)
        if re.fullmatch(r'[A-Za-z0-9_-]{6,20}', src):
            return src
        return ''

    def youtube_embed_url(self) -> str:
        """Player URL for the slot, clipped if a start or end was given.

        youtube-nocookie.com, and never autoplaying with sound: an ad that
        shouts at somebody mid-quiz is worse than no ad.
        """
        vid = self.youtube_id()
        if not vid:
            return ''
        params = [
            'rel=0', 'modestbranding=1', 'playsinline=1', 'iv_load_policy=3',
        ]
        start = max(0, int(self.video_start or 0))
        end = max(0, int(self.video_end or 0))
        if start:
            params.append('start=%d' % start)
        if end and end > start:
            params.append('end=%d' % end)
        return 'https://www.youtube-nocookie.com/embed/%s?%s' % (vid, '&'.join(params))

    def is_live(self, now=None) -> bool:
        """Should this be served right now?"""
        now = now or datetime.utcnow()
        if not self.is_active or not self.approved_family:
            return False
        if self.starts_at and now < self.starts_at:
            return False
        if self.ends_at and now > self.ends_at:
            return False
        if self.kind == 'image' and not self.image_url:
            return False
        if self.kind == 'youtube' and not self.youtube_id():
            return False
        if self.kind == 'adsense' and not self.adsense_slot_id:
            return False
        return True

    def click_rate(self) -> float:
        """Clicks per hundred impressions, which is what an advertiser asks for."""
        if not self.impressions:
            return 0.0
        return round((self.clicks or 0) * 100.0 / self.impressions, 2)

    def status_label(self) -> str:
        if not self.approved_family:
            return 'Awaiting review'
        if not self.is_active:
            return 'Paused'
        now = datetime.utcnow()
        if self.starts_at and now < self.starts_at:
            return 'Scheduled'
        if self.ends_at and now > self.ends_at:
            return 'Finished'
        return 'Live'


class AdStat(db.Model):
    """One row per ad per day, so a report can show a run rather than a total."""
    __tablename__ = 'ad_stats'
    __table_args__ = (db.UniqueConstraint('ad_id', 'day', name='uq_ad_stat_day'),)

    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('advertisements.id'), index=True, nullable=False)
    day = db.Column(db.Date, index=True, nullable=False)
    impressions = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)


class SsoUsedNonce(db.Model):
    __tablename__ = 'sso_used_nonce'

    nonce = db.Column(db.String(64), primary_key=True)
    expires_at = db.Column(db.Integer, nullable=False, index=True)
    used_at = db.Column(db.DateTime, default=datetime.utcnow)

class ClimberSeason(db.Model):
    """Monthly Expedition Season for The Quiz Climber challenge."""
    __tablename__ = 'climber_seasons'

    id = db.Column(db.Integer, primary_key=True)
    month_key = db.Column(db.String(10), unique=True, index=True, nullable=False)  # e.g. '2026-11'
    title = db.Column(db.String(120), default='Everest North Ridge Expedition')
    mountain_name = db.Column(db.String(80), default='Mount Everest')
    elevation_m = db.Column(db.Integer, default=8848)
    sponsor_name = db.Column(db.String(100), default='Peak Performance Gear')
    sponsor_url = db.Column(db.String(255), default='/posts')
    sponsor_article_slug = db.Column(db.String(150), default='')
    starts_at = db.Column(db.DateTime, default=datetime.utcnow)
    ends_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ClimberProgress(db.Model):
    """User progress along the vertical rock face for the active 30-day Climber season."""
    __tablename__ = 'climber_progress'

    id = db.Column(db.Integer, primary_key=True)
    player_profile_id = db.Column(db.Integer, db.ForeignKey('player_profiles.id'), index=True, nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('climber_seasons.id'), index=True, nullable=False)
    current_stage = db.Column(db.Integer, default=1)  # 1: Basecamp, 2: Khumbu, 3: Camp 2, 4: Lhotse, 5: South Col, 6: Summit
    current_day = db.Column(db.Integer, default=1)    # Day 1-30 of the expedition
    current_step = db.Column(db.Integer, default=1)   # Step 1-30 overall
    secured_camp_stage = db.Column(db.Integer, default=1) # Permanent Safe Haven Camp reached
    altitude_m = db.Column(db.Integer, default=1000)
    banked_coins = db.Column(db.Integer, default=0)
    unbanked_coins = db.Column(db.Integer, default=0)
    highest_altitude = db.Column(db.Integer, default=1000)
    status = db.Column(db.String(20), default='climbing')  # climbing, summit, banked, fallen
    total_falls = db.Column(db.Integer, default=0)
    total_summits = db.Column(db.Integer, default=0)
    last_question_id = db.Column(db.Integer, nullable=True)
    last_climbed_date = db.Column(db.Date, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserPostRead(db.Model):
    """Record of verified article dwell time rewards (Field Intel Recon)."""
    __tablename__ = 'user_post_reads'

    id = db.Column(db.Integer, primary_key=True)
    player_profile_id = db.Column(db.Integer, db.ForeignKey('player_profiles.id'), index=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), index=True, nullable=False)
    coins_awarded = db.Column(db.Integer, default=25)
    read_seconds = db.Column(db.Integer, default=15)
    claimed_at = db.Column(db.DateTime, default=datetime.utcnow)

class ClimberFact(db.Model):
    """Historical, terrain, and mountaineering facts unlocked during the 30-day expedition."""
    __tablename__ = 'climber_facts'

    id = db.Column(db.Integer, primary_key=True)
    stage_number = db.Column(db.Integer, default=1, index=True)  # 1 to 6
    altitude_m = db.Column(db.Integer, default=1000)
    title = db.Column(db.String(120), nullable=False)
    fact_text = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(20), default='⛰️')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserClimberFactSeen(db.Model):
    """Tracks which mountain facts a player has already seen across all months to prevent repeats."""
    __tablename__ = 'user_climber_facts_seen'

    id = db.Column(db.Integer, primary_key=True)
    player_profile_id = db.Column(db.Integer, db.ForeignKey('player_profiles.id'), index=True, nullable=False)
    fact_id = db.Column(db.Integer, db.ForeignKey('climber_facts.id'), index=True, nullable=False)
    seen_at = db.Column(db.DateTime, default=datetime.utcnow)

