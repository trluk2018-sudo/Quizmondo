import os
from datetime import timedelta
from flask import Flask, send_from_directory, redirect, url_for, session, request
from .models import db, User, SiteSetting, Category, Page, Post, MenuItem, SidebarWidget, PageModule, PlayerProfile


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Resolve platform / tenant environment configurations
    secret_key = os.environ.get('APP_SECRET_KEY') or os.environ.get('SECRET_KEY') or 'sitebuilder-express-insecure-dev-key'
    db_url = os.environ.get('APP_DATABASE_URL') or os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(app.instance_path, 'sitebuilder.sqlite')}"
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)

    upload_dir = os.environ.get('APP_UPLOAD_DIR') or os.path.join(app.instance_path, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Configuration defaults
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB file upload limit
        APP_PUBLIC_URL=os.environ.get('APP_PUBLIC_URL', 'http://localhost:8000'),
        APP_SSO_SECRET=os.environ.get('APP_SSO_SECRET') or os.environ.get('SSO_SECRET', ''),
        UPLOAD_FOLDER=upload_dir,
        PERMANENT_SESSION_LIFETIME=timedelta(days=30),
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_PATH='/'
    )

    if test_config:
        app.config.update(test_config)

    # Init database
    db.init_app(app)

    # High-concurrency SQLite tuning (WAL mode, busy_timeout, cache) for 100s of concurrent players
    try:
        from sqlalchemy import event
        from sqlalchemy.engine import Engine

        @event.listens_for(Engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            if db_url.startswith('sqlite'):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA journal_mode=WAL;")
                cursor.execute("PRAGMA synchronous=NORMAL;")
                cursor.execute("PRAGMA busy_timeout=15000;")
                cursor.execute("PRAGMA cache_size=-32000;")
                cursor.close()
    except Exception:
        pass

    @app.before_request
    def ensure_persistent_login_state():
        """Keep player and admin login state rock-solid across all pages, tabs, and duels."""
        if request.endpoint and request.endpoint.startswith('static'):
            return
        session.permanent = True
        uid = session.get('user_id')
        if uid:
            user = db.session.get(User, uid)
            if user and user.is_active:
                session['username'] = user.username
                session['user_role'] = user.role or 'player'
                session['is_creator'] = user.role in ('super_admin', 'admin', 'quizmaster', 'creator')
                prof = PlayerProfile.query.filter_by(user_id=user.id).first()
                if prof:
                    if prof.display_name != user.username:
                        prof.display_name = user.username
                        db.session.commit()
                    session['qm_player_key'] = prof.session_key
            else:
                session.pop('user_id', None)
                session.pop('username', None)
                session.pop('user_role', None)
                session.pop('is_creator', None)

    # Persistent upload handlers
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/static/uploads/<path:filename>')
    def serve_static_upload(filename):
        # Fallback to UPLOAD_FOLDER or static uploads
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        static_uploads = os.path.join(app.static_folder, 'uploads')
        return send_from_directory(static_uploads, filename)

    # Root SSO entrypoints (direct from SaaS Control Plane)
    @app.route('/sso')
    def root_sso():
        from .routes.auth import handle_sso
        return handle_sso()

    @app.route('/end-impersonation')
    def root_end_impersonation():
        from .routes.auth import end_impersonation_handler
        return end_impersonation_handler()

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.public import public_bp
    from .routes.arena import arena_bp
    from .routes.games import games_bp
    from .routes.account import account_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(arena_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(account_bp)

    @app.after_request
    def never_cache_pages(response):
        """Serve pages fresh, and let static files keep their caching.

        Every mini game's JavaScript is inline in its own page, so a cached
        page is cached gameplay: a deploy that fixes a game changes nothing on
        a phone still holding yesterday's HTML, and the fix looks as though it
        did not work. That has already cost an afternoon of chasing a bug that
        was fixed on the server the whole time.

        Only HTML is covered. Caching earns its keep on the CSS, the images
        and the word list, and none of those are touched here.
        """
        if response.mimetype == 'text/html':
            response.headers['Cache-Control'] = 'no-store, max-age=0, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
        return response

    import re
    @app.template_filter('youtube_id')
    def youtube_id_filter(url):
        if not url:
            return ''
        url = str(url).strip()
        patterns = [
            r'(?:v=|\/embed\/|\.be\/|youtu\.be\/|\/v\/)([0-9A-Za-z_-]{11})',
            r'^([0-9A-Za-z_-]{11})$'
        ]
        for p in patterns:
            m = re.search(p, url)
            if m:
                return m.group(1)
        return ''

    @app.template_filter('rgba')
    def rgba_filter(hex_color, opacity=100):
        if not hex_color or hex_color in ('default', 'transparent'):
            return hex_color or ''
        hex_code = str(hex_color).strip().lstrip('#')
        if len(hex_code) == 3:
            hex_code = ''.join([c*2 for c in hex_code])
        if len(hex_code) != 6:
            return str(hex_color)
        try:
            r = int(hex_code[0:2], 16)
            g = int(hex_code[2:4], 16)
            b = int(hex_code[4:6], 16)
            alpha = max(0.0, min(1.0, float(opacity) / 100.0))
            return f"rgba({r}, {g}, {b}, {alpha:.2f})"
        except Exception:
            return f"#{hex_code}"

    # Database setup & initial seed
    with app.app_context():
        db.create_all()
        _ensure_schema()
        _seed_defaults()

    return app


def _ensure_schema():
    """Ensure newly introduced columns exist in SQLite without requiring manual migrations."""
    try:
        from sqlalchemy import text
        cols_pages = [row[1] for row in db.session.execute(text("PRAGMA table_info(pages)")).fetchall()]
        if cols_pages:
            if 'excerpt' not in cols_pages:
                db.session.execute(text("ALTER TABLE pages ADD COLUMN excerpt TEXT DEFAULT ''"))
            if 'meta_title' not in cols_pages:
                db.session.execute(text("ALTER TABLE pages ADD COLUMN meta_title VARCHAR(255) DEFAULT ''"))
            if 'meta_description' not in cols_pages:
                db.session.execute(text("ALTER TABLE pages ADD COLUMN meta_description TEXT DEFAULT ''"))
            if 'meta_keywords' not in cols_pages:
                db.session.execute(text("ALTER TABLE pages ADD COLUMN meta_keywords VARCHAR(255) DEFAULT ''"))
            if 'canonical_url' not in cols_pages:
                db.session.execute(text("ALTER TABLE pages ADD COLUMN canonical_url VARCHAR(500) DEFAULT ''"))
            if 'og_image' not in cols_pages:
                db.session.execute(text("ALTER TABLE pages ADD COLUMN og_image VARCHAR(500) DEFAULT ''"))
            if 'no_index' not in cols_pages:
                db.session.execute(text("ALTER TABLE pages ADD COLUMN no_index BOOLEAN DEFAULT 0"))
            db.session.commit()

        cols_posts = [row[1] for row in db.session.execute(text("PRAGMA table_info(posts)")).fetchall()]
        if cols_posts:
            if 'meta_title' not in cols_posts:
                db.session.execute(text("ALTER TABLE posts ADD COLUMN meta_title VARCHAR(255) DEFAULT ''"))
            if 'meta_description' not in cols_posts:
                db.session.execute(text("ALTER TABLE posts ADD COLUMN meta_description TEXT DEFAULT ''"))
            if 'meta_keywords' not in cols_posts:
                db.session.execute(text("ALTER TABLE posts ADD COLUMN meta_keywords VARCHAR(255) DEFAULT ''"))
            if 'canonical_url' not in cols_posts:
                db.session.execute(text("ALTER TABLE posts ADD COLUMN canonical_url VARCHAR(500) DEFAULT ''"))
            if 'og_image' not in cols_posts:
                db.session.execute(text("ALTER TABLE posts ADD COLUMN og_image VARCHAR(500) DEFAULT ''"))
            if 'no_index' not in cols_posts:
                db.session.execute(text("ALTER TABLE posts ADD COLUMN no_index BOOLEAN DEFAULT 0"))
            if 'pin_order' not in cols_posts:
                db.session.execute(text("ALTER TABLE posts ADD COLUMN pin_order INTEGER DEFAULT 0"))
            db.session.commit()

        cols_menu = [row[1] for row in db.session.execute(text("PRAGMA table_info(menu_items)")).fetchall()]
        if cols_menu and 'parent_id' not in cols_menu:
            db.session.execute(text("ALTER TABLE menu_items ADD COLUMN parent_id INTEGER REFERENCES menu_items(id)"))
            db.session.commit()

        cols_widgets = [row[1] for row in db.session.execute(text("PRAGMA table_info(sidebar_widgets)")).fetchall()]
        if cols_widgets and 'config_json' not in cols_widgets:
            db.session.execute(text("ALTER TABLE sidebar_widgets ADD COLUMN config_json TEXT DEFAULT '{}'"))
            db.session.commit()

        cols_modules = [row[1] for row in db.session.execute(text("PRAGMA table_info(page_modules)")).fetchall()]
        if cols_modules and 'theme' not in cols_modules:
            db.session.execute(text("ALTER TABLE page_modules ADD COLUMN theme VARCHAR(50) DEFAULT 'hisoft'"))
            db.session.commit()

        cols_profiles = [row[1] for row in db.session.execute(text("PRAGMA table_info(player_profiles)")).fetchall()]
        if cols_profiles:
            if 'is_paused' not in cols_profiles:
                db.session.execute(text("ALTER TABLE player_profiles ADD COLUMN is_paused BOOLEAN DEFAULT 0"))
            if 'is_anonymised' not in cols_profiles:
                db.session.execute(text("ALTER TABLE player_profiles ADD COLUMN is_anonymised BOOLEAN DEFAULT 0"))
            db.session.commit()

        cols_leagues = [row[1] for row in db.session.execute(text("PRAGMA table_info(pub_leagues)")).fetchall()]
        if cols_leagues and 'teams_json' not in cols_leagues:
            db.session.execute(text("ALTER TABLE pub_leagues ADD COLUMN teams_json TEXT DEFAULT '[]'"))
            db.session.commit()
        cols_featured = [row[1] for row in db.session.execute(text("PRAGMA table_info(featured_games)")).fetchall()]
        if cols_featured:
            if 'video_url' not in cols_featured:
                db.session.execute(text("ALTER TABLE featured_games ADD COLUMN video_url VARCHAR(500) DEFAULT ''"))
            if 'video_start' not in cols_featured:
                db.session.execute(text("ALTER TABLE featured_games ADD COLUMN video_start INTEGER DEFAULT 0"))
            if 'video_end' not in cols_featured:
                db.session.execute(text("ALTER TABLE featured_games ADD COLUMN video_end INTEGER DEFAULT 0"))
            db.session.commit()

        if cols_leagues and 'is_virtual' not in cols_leagues:
            db.session.execute(text("ALTER TABLE pub_leagues ADD COLUMN is_virtual BOOLEAN"))
            db.session.commit()
            # Seed the new flag from the old naming heuristic so every league keeps the mode it has today
            from .models import PubLeague
            for lg in PubLeague.query.all():
                lg.is_virtual = lg.looks_virtual()
            db.session.commit()

        cols_questions = [row[1] for row in db.session.execute(text("PRAGMA table_info(quiz_questions)")).fetchall()]
        if cols_questions:
            if 'status' not in cols_questions:
                db.session.execute(text("ALTER TABLE quiz_questions ADD COLUMN status VARCHAR(20) DEFAULT 'approved'"))
            if 'is_community' not in cols_questions:
                db.session.execute(text("ALTER TABLE quiz_questions ADD COLUMN is_community BOOLEAN DEFAULT 0"))
            db.session.commit()

        # High-concurrency composite indexes for matchmaking, round lookup, and visual question selection
        db.session.execute(text("CREATE INDEX IF NOT EXISTS ix_qq_cat_type_diff ON quiz_questions (category_slug, question_type, difficulty)"))
        db.session.execute(text("CREATE INDEX IF NOT EXISTS ix_am_p1_status ON arena_matches (player1_session, status)"))
        db.session.execute(text("CREATE INDEX IF NOT EXISTS ix_am_p2_status ON arena_matches (player2_session, status)"))
        db.session.execute(text("CREATE INDEX IF NOT EXISTS ix_ar_match_round ON arena_rounds (match_id, round_number)"))
        db.session.execute(text("CREATE INDEX IF NOT EXISTS ix_pp_xp ON player_profiles (xp DESC)"))
        db.session.commit()
    except Exception:
        db.session.rollback()


def _seed_defaults():
    # Admin user credentials from environment or defaults
    admin_user = os.environ.get('APP_ADMIN_USER', 'admin')
    admin_pass = os.environ.get('APP_ADMIN_PASSWORD', 'admin123')
    admin_email = os.environ.get('APP_ADMIN_EMAIL', f'{admin_user}@sitebuilder.local')
    company_name = os.environ.get('APP_COMPANY_NAME')

    # Create default admin if no users exist
    if not User.query.first():
        admin = User(username=admin_user, email=admin_email, role='admin')
        admin.set_password(admin_pass)
        db.session.add(admin)

    # Seed default settings tailored for Quizmondo Arena
    site_title = company_name if company_name else 'Quizmondo'
    defaults = {
        'site_title': site_title,
        'site_tagline': 'Interactive Live Quizzes, Gaming Arena & Brain Tournaments',
        'active_theme': 'quizhub',
        'home_hero_title': 'Battle Live in the Ultimate Trivia & Brain Gaming Arena',
        'home_hero_subtitle': 'Test your knowledge across 50+ categories, compete in live tournaments for real prize pools, and climb global leaderboards.',
        'home_hero_button_label': 'Play Daily Challenge',
        'home_hero_button_url': '/#services',
        'home_modules_json': '["hero", "features_strip", "about", "services", "case_studies", "posts", "testimonials", "trust_strip", "contact"]',
        'layout_accent_color': '#8b5cf6',
        'contact_phone': '+44 (0) 20 7946 0912',
        'contact_email': 'arena@quizmondo.com',
        'contact_address': 'Arena Hub, London EC2A 4NE',
        'homepage_type': 'posts',
        'posts_per_page': '10',
        'site_logo': '/static/img/quizmondo_logo.svg',
        'header_style': 'split_nav',
        'header_bg_color': '#0f0728',
        'header_bg_opacity': '100',
        'header_text_color': '#f3e8ff',
        'header_text_opacity': '100',
        'header_accent_color': '#8b5cf6',
        'header_accent_opacity': '100',
        'header_font_style': 'bold-display',
        'header_show_topbar': '1',
        'header_cta_text': 'Join Arena',
        'header_cta_url': '/arena',
        'footer_bg_color': '#090317',
        'footer_bg_opacity': '100',
        'footer_text_color': '#d8b4fe',
        'footer_text_opacity': '100',
        'footer_accent_color': '#06b6d4',
        'footer_accent_opacity': '100',
        'footer_logo': '/static/img/quizmondo_logo.svg',
        'footer_about_text': 'Quizmondo is the premier competitive brain gaming platform featuring real-time multiplayer showdowns, cash tournaments, and adaptive trivia challenges.',
        'footer_copyright': '© 2026 Quizmondo.com. All rights reserved.',
    }
    for k, v in defaults.items():
        existing = SiteSetting.query.filter_by(key=k).first()
        if not existing:
            db.session.add(SiteSetting(key=k, value=v))
        elif k in ('site_logo', 'footer_logo', 'active_theme'):
            existing.value = v
        elif k == 'header_cta_url' and existing.value == '/contact':
            # Correct the one bad default without overriding a destination chosen since
            existing.value = v

    # Seed Quizmondo Arena initial question packs, leagues, and homepage modules
    from .utils.quiz_seed import seed_quizmondo_full_environment
    seed_quizmondo_full_environment()

    # Seed initial categories for Quizmondo
    cat_science = Category.query.filter_by(slug='science-cosmos').first()
    if not cat_science:
        cat_science = Category(name='Science & Cosmos', slug='science-cosmos', description='Astrophysics, planetary science, and cosmology trivia.')
        db.session.add(cat_science)

    cat_gaming = Category.query.filter_by(slug='gaming-esports').first()
    if not cat_gaming:
        cat_gaming = Category(name='Gaming & Esports', slug='gaming-esports', description='Retro gaming lore, speedruns, and tournament breakdowns.')
        db.session.add(cat_gaming)

    cat_world = Category.query.filter_by(slug='world-history').first()
    if not cat_world:
        cat_world = Category(name='World Trivia', slug='world-history', description='Historical mysteries, global landmarks, and cultural puzzles.')
        db.session.add(cat_world)

    db.session.commit()

    # Seed sample trivia posts for Quizmondo
    if not Post.query.first():
        p1 = Post(
            title='Which Planet Has the Most Moons? Saturn Overtakes Jupiter in Latest Astronomy Count',
            slug='which-planet-has-the-most-moons-saturn-jupiter',
            content='<p>For years, Jupiter and Saturn have traded the crown of the Solar System\'s moon king. With the recent discovery of 62 new irregular moons, Saturn now commands an astonishing 146 confirmed satellites.</p><p>Explore the cosmic trivia behind gas giants and how automated telescopes are reshaping planetary cartography.</p>',
            excerpt='Saturn officially reclaimed the cosmic title with 146 confirmed moons. Discover the fascinating trivia behind our Solar System giants.',
            category_id=cat_science.id,
            status='publish'
        )
        p2 = Post(
            title='The Evolution of Speedruns: Breaking Impossible Video Game Records',
            slug='evolution-of-speedruns-breaking-impossible-records',
            content='<p>From frame-perfect glitches to sub-pixel maneuvers, competitive gaming speedrunners push classical physics engines beyond designed limits.</p><p>We examine the history of live marathon tournaments and how millions watch world records shatter in real-time.</p>',
            excerpt='How sub-pixel manipulation and relentless practice revolutionized competitive speedrunning communities worldwide.',
            category_id=cat_gaming.id,
            status='publish'
        )
        p3 = Post(
            title='Ancient Enigmas: 7 Historical Trivia Facts That Sound Completely Fake',
            slug='ancient-enigmas-historical-trivia-facts',
            content='<p>Did you know Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramids? Dive into our top brain-twisting historical trivia facts verified by historians.</p>',
            excerpt='Test your intuition with 7 astonishing historical milestones that defy conventional timelines.',
            category_id=cat_world.id,
            status='publish'
        )
        db.session.add_all([p1, p2, p3])

    # Seed default pages (About and Contact)
    about_page = Page.query.filter_by(slug='about').first()
    if not about_page:
        about_page = Page(
            title='About Quizmondo Arena',
            slug='about',
            content='<p>Quizmondo is the ultimate interactive gaming and esports trivia battleground featuring live challenges and global leaderboard rankings.</p><h2>Our Philosophy</h2><p>We blend competitive gaming excitement with brain training, giving trivia lovers everywhere an authentic platform to test their wits.</p>',
            template='default',
            status='publish',
            sort_order=1
        )
        db.session.add(about_page)

    # Legal pages. Seeded once so they are editable in Admin > Pages like any other page
    # rather than baked into a template.
    terms_page = Page.query.filter_by(slug='terms').first()
    if not terms_page:
        db.session.add(Page(
            title='Terms & Conditions',
            slug='terms',
            excerpt='Quizmondo is free to use and provided as-is. These are the rules of the house.',
            content="""<p><strong>Quizmondo is free to use, and it is run as a hobby project.</strong> These terms set out what that means in practice. By playing, you accept them.</p>

<h2>1. The service is free, and provided as-is</h2>
<p>There is no charge to play Quizmondo and no subscription. In return, the service comes with no guarantees. It may be slow, it may be unavailable, questions may contain mistakes, and scores or accounts may occasionally be lost. We make no promise that the site will be available at any particular time or that any feature will keep working.</p>

<h2>2. It can be withdrawn or changed at any time</h2>
<p>We may change, suspend, restrict or shut down Quizmondo, in whole or in part, at any time and without notice. That includes removing features, resetting leaderboards and league tables, deleting inactive accounts, or ending the service altogether. Because the service is free, no refund or compensation arises in any of these cases.</p>

<h2>3. Fair use, and what counts as abuse</h2>
<p>Use Quizmondo the way it is meant to be used. You must not:</p>
<ul>
<li>cheat, manipulate scores, or use scripts, bots or automated tools to play, except the in-game bots we provide;</li>
<li>attempt to access accounts, data or parts of the system that are not yours;</li>
<li>probe, scan, overload or attack the service, or make excessive automated requests;</li>
<li>submit community questions or team, squad or player names that are abusive, hateful, obscene, defamatory, or that infringe someone else's rights;</li>
<li>harass other players, including through names, messages or invitations;</li>
<li>copy, scrape or republish the question bank or other site content for your own service;</li>
<li>use the service for anything unlawful.</li>
</ul>
<p>We may remove content, suspend or delete accounts, and block access, at our discretion and without notice, where we believe these rules have been broken. We do not have to explain the decision.</p>

<h2>4. Your account</h2>
<p>You are responsible for your account and for keeping your PIN or password to yourself. Do not share it. Tell us if you think someone else has access. You may stop using the service at any time, and you may ask us to delete your account.</p>

<h2>5. Content you submit</h2>
<p>If you write quiz questions, team names or other content, you confirm it is yours to submit and does not infringe anyone's rights. You keep ownership of it, and you give us permission to host, display and use it within Quizmondo. We may edit or remove anything submitted, including through our moderation queue.</p>

<h2>6. Quizzes, prizes and pub leagues</h2>
<p>Where a venue runs a pub quiz through Quizmondo, any prize is the venue's and nothing to do with us. We provide the software only. We are not responsible for how a quiz is run, how it is scored in the room, or any prize that is or is not awarded.</p>

<h2>7. Accuracy of questions</h2>
<p>We try to get questions and answers right, but trivia is trivia and errors happen. Nothing on Quizmondo should be relied on as factual, professional or any other kind of advice.</p>

<h2>8. Liability</h2>
<p>To the extent the law allows, we accept no liability for any loss or damage arising from your use of Quizmondo, including lost scores, lost accounts, lost data or unavailability of the service. Nothing in these terms limits liability for death or personal injury caused by negligence, for fraud, or for anything else that cannot lawfully be limited.</p>

<h2>9. Children</h2>
<p>Quizmondo is intended for general audiences. If you are under 13, please ask a parent or guardian before creating an account.</p>

<h2>10. Changes to these terms</h2>
<p>We may update these terms. The version on this page is the one that applies. Continuing to use the service after a change means you accept the new version.</p>

<h2>11. Governing law</h2>
<p>These terms are governed by the law of England and Wales, and the courts of England and Wales have jurisdiction.</p>

<h2>Contact</h2>
<p>Questions about these terms can be sent through the <a href="/contact">contact page</a>.</p>""",
            template='default', status='publish', sort_order=90
        ))

    privacy_page = Page.query.filter_by(slug='privacy').first()
    privacy_body = """<p class="lead">This notice explains what personal data Quizmondo collects, why, what we do with it, and the rights you have over it. It is written to meet Articles 13 and 14 of the UK GDPR. We collect as little as we can.</p>
<p><em>Last updated: 28 October 2026.</em></p>

<h2>1. Who is the data controller</h2>
<p>Quizmondo operates this website and is the <strong>data controller</strong> for the personal data described below. You can reach us about anything on this page through the <a href="/contact">contact page</a>. We have not appointed a Data Protection Officer, as we are not required to.</p>

<h2>2. What personal data we collect</h2>
<p>If you create an account we store exactly three pieces of personal data:</p>
<table>
<tr><th>What</th><th>Why we need it</th></tr>
<tr><td><strong>Player name</strong></td><td>To identify you in games and show you on leaderboards. It need not be your real name, and we would prefer it was not.</td></tr>
<tr><td><strong>Email address</strong></td><td>To identify your account so you can sign back in, and to reply if you contact us.</td></tr>
<tr><td><strong>PIN or password</strong></td><td>To secure your account. Stored only as a one-way cryptographic hash, never in readable form. Nobody at Quizmondo can see it.</td></tr>
</table>
<p>We do <strong>not</strong> collect your real name, postal address, date of birth, telephone number, payment details or location. We have no use for them. There is no advertising on Quizmondo and we do not sell data to anyone.</p>

<h3>Data created by playing</h3>
<p>Using the site also generates records linked to your account: scores, XP and rank, the duels and group games you play, quiz questions or team names you submit, and pub quiz results recorded under the team name used on the night. Some of this is shown publicly &mdash; that is the purpose of a leaderboard.</p>

<h3>Playing without an account</h3>
<p>You can play entirely as a guest. A guest is identified only by a random key held in your own browser with a generated display name; we hold no email or password for you. Clearing your browser data removes that identity and its scores permanently.</p>

<h2>3. Our lawful basis for processing</h2>
<table>
<tr><th>Processing</th><th>Lawful basis (UK GDPR Article 6)</th></tr>
<tr><td>Holding your account so you can sign in and play</td><td>Article 6(1)(b) &mdash; performance of a contract with you</td></tr>
<tr><td>Showing player names and scores on leaderboards</td><td>Article 6(1)(f) &mdash; legitimate interests: running a competitive quiz service that works as players expect</td></tr>
<tr><td>Keeping the service secure and preventing cheating or abuse</td><td>Article 6(1)(f) &mdash; legitimate interests: protecting the service and its players</td></tr>
<tr><td>Replying to a message you send us</td><td>Article 6(1)(f) &mdash; legitimate interests: answering your enquiry</td></tr>
<tr><td>Optional website analytics, where enabled</td><td>Article 6(1)(a) &mdash; consent, which you may withdraw at any time</td></tr>
</table>
<p>Providing this data is not a statutory requirement. It is required only to hold an account: without an email address and a PIN there is no way to sign you back in. You may always play as a guest instead.</p>

<h2>4. Who we share it with</h2>
<p>We do not sell, rent or trade your personal data, and we do not share it for marketing. It is stored on hosting infrastructure operated by our hosting provider, which acts as a <strong>data processor</strong> and handles it only on our instructions in order to run the site. Your player name and scores are visible to other players in the ordinary course of play: leaderboards, duel results, group games and pub league tables. We will disclose data where the law requires it.</p>

<h2>5. International transfers</h2>
<p>Our hosting is within the UK or the European Economic Area. If that ever changes, transfers will be made only to a country with UK adequacy status or under appropriate safeguards such as the International Data Transfer Agreement, and this notice will be updated to say so.</p>

<h2>6. How long we keep it</h2>
<ul>
<li><strong>Account data</strong> is kept for as long as your account exists. Ask us to delete it and we delete it.</li>
<li><strong>Inactive accounts</strong> may be removed after a long period of no activity.</li>
<li><strong>Pub league results</strong> are retained as a historical record of a competition, under the team name used that night.</li>
<li><strong>Messages you send us</strong> are kept only as long as needed to deal with them.</li>
</ul>

<h2>7. Your rights, and how to use them</h2>
<p>Under the UK GDPR you have the following rights. All of them are free, and we will respond within <strong>one month</strong>.</p>
<ul>
<li><strong>Right of access (Article 15).</strong> Ask what we hold about you and get a copy.</li>
<li><strong>Right to rectification (Article 16).</strong> Have anything inaccurate corrected. You can change your player name yourself at any time.</li>
<li><strong>Right to erasure (Article 17).</strong> Have your personal data deleted &mdash; see below.</li>
<li><strong>Right to restrict processing (Article 18).</strong> Ask us to stop using your data while a dispute is resolved.</li>
<li><strong>Right to data portability (Article 20).</strong> Receive the data you gave us in a structured, machine-readable format.</li>
<li><strong>Right to object (Article 21).</strong> Object to processing we carry out under legitimate interests, including appearing on public leaderboards.</li>
<li><strong>Right to withdraw consent (Article 7).</strong> Where we rely on consent, withdraw it at any time without affecting what was done beforehand.</li>
</ul>
<p>To use any of these, write to us through the <a href="/contact">contact page</a> from the email address on your account, or tell us the player name concerned. We may need to confirm it is really you before acting, so that somebody else cannot delete your account.</p>

<h3>Deleting your account and your data</h3>
<p>You have the right to have your personal data erased, and you do not have to give a reason. On request we will, within one month:</p>
<ul>
<li>delete your <strong>email address</strong>;</li>
<li>delete your <strong>player name</strong>;</li>
<li>delete your <strong>stored PIN or password hash</strong>;</li>
<li>delete the account itself, so it can no longer be signed into.</li>
</ul>
<p>We will also remove your player name from leaderboards and from duel and group game records, or replace it with an anonymous label where a record of the game itself has to remain so that other players' results still make sense. Once a name has been removed in this way the remaining record is no longer personal data and cannot be traced back to you.</p>
<p>One honest exception: a pub quiz result recorded under a <em>team</em> name, which is usually shared by several people and is not normally personal data, is kept as the historical record of that competition. If a team name does identify you, tell us and we will change or remove it.</p>
<p>Erasure is permanent. Scores, XP and rank cannot be recovered afterwards.</p>

<h2>8. Cookies and browser storage</h2>
<p>We use a <strong>session cookie</strong> to keep you signed in and to remember which table or squad you joined. The game screens use your browser's <strong>local storage</strong> to hold your place in a round, so refreshing the page or losing signal does not cost you your answers. Both are strictly necessary for the site to work and neither is used for advertising or cross-site tracking.</p>
<p>If website analytics are switched on by the site owner, that provider may set its own cookies. Where that happens it is disclosed here and relies on your consent.</p>

<h2>9. Automated decision-making</h2>
<p>We do not carry out profiling or automated decision-making that produces legal or similarly significant effects. Scoring a quiz is automated, but it only decides who won a quiz.</p>

<h2>10. Security</h2>
<p>PINs and passwords are stored only as one-way hashes, and the site is served over HTTPS. No system is completely secure, so please use a PIN you do not use anywhere else.</p>

<h2>11. Children</h2>
<p>Quizmondo is intended for general audiences. If you are under 13, please ask a parent or guardian before creating an account. If you believe a child has provided us with personal data without that permission, contact us and we will delete it.</p>

<h2>12. Complaints</h2>
<p>If you are unhappy with how we have handled your personal data, please tell us first so we can put it right. You also have the right to complain to the UK supervisory authority, the Information Commissioner's Office, at <a href="https://ico.org.uk" target="_blank" rel="noopener">ico.org.uk</a> or on 0303 123 1113.</p>

<h2>13. Changes to this notice</h2>
<p>If what we collect or what we do with it changes, this page is updated and the date at the top changes with it."""
    if not privacy_page:
        db.session.add(Page(
            title='Privacy & Your Data',
            slug='privacy',
            excerpt='What we collect, which is a player name, an email address and a hashed PIN, and nothing else. Including how to have it all deleted.',
            content=privacy_body,
            template='default', status='publish', sort_order=91
        ))
    elif 'We collect as little as we can get away with' in (privacy_page.content or ''):
        # The first version of this page was a plain-English summary rather than a
        # compliant notice. Upgrade it in place, but only while it is word for word
        # that version - keyed on a phrase unique to it - so that any edit made in
        # the admin, however small, is left alone.
        privacy_page.content = privacy_body
        privacy_page.excerpt = ('What we collect, which is a player name, an email address and a hashed PIN, '
                                'and nothing else. Including how to have it all deleted.')

    contact_page = Page.query.filter_by(slug='contact').first()
    if not contact_page:
        contact_page = Page(
            title='Support & Arena Concierge',
            slug='contact',
            content='<p>Have inquiries about live tournaments, enterprise quiz nights, or leaderboard verification? Get in touch with our operations team.</p>',
            template='contact',
            status='publish',
            sort_order=2
        )
        db.session.add(contact_page)

    # Seed default header menu
    if not MenuItem.query.first():
        db.session.add(MenuItem(title='Arena Home', url='/', location='header', sort_order=1))
        db.session.add(MenuItem(title='Game Modes', url='/#services', location='header', sort_order=2))
        db.session.add(MenuItem(title='Battle Guides', url='/posts', location='header', sort_order=3))
        db.session.add(MenuItem(title='Arena Rules', url='/about', location='header', sort_order=4))
        db.session.add(MenuItem(title='Support Desk', url='/contact', location='header', sort_order=5))

        db.session.add(MenuItem(title='Arena Home', url='/', location='footer', sort_order=1))
        db.session.add(MenuItem(title='Game Modes', url='/#services', location='footer', sort_order=2))
        db.session.add(MenuItem(title='Battle Guides', url='/posts', location='footer', sort_order=3))
        db.session.add(MenuItem(title='Arena Rules', url='/about', location='footer', sort_order=4))
        db.session.add(MenuItem(title='Support Desk', url='/contact', location='footer', sort_order=5))

    # Seed default disciplines/modes menu items if not already present
    if not MenuItem.query.filter_by(location='solutions').first():
        db.session.add(MenuItem(title='Daily Brain Challenge', url='/#services', location='solutions', sort_order=1))
        db.session.add(MenuItem(title='Multiplayer eSports Leagues', url='/#services', location='solutions', sort_order=2))
        db.session.add(MenuItem(title='Science & Tech Cups', url='/#services', location='solutions', sort_order=3))
        db.session.add(MenuItem(title='Pop Culture & Cinema Faceoff', url='/#services', location='solutions', sort_order=4))
        db.session.add(MenuItem(title='Corporate Team Quiz Arenas', url='/#services', location='solutions', sort_order=5))

    # Seed default sidebar widgets
    if not SidebarWidget.query.filter_by(sidebar_id='sidebar-right').first():
        db.session.add(SidebarWidget(
            sidebar_id='sidebar-right',
            widget_type='recent_posts',
            title='Recent Dispatches',
            sort_order=1
        ))
        db.session.add(SidebarWidget(
            sidebar_id='sidebar-right',
            widget_type='categories',
            title='Practice Areas',
            sort_order=2
        ))

    # Seed default 4-column footer widgets if none exist yet
    if not SidebarWidget.query.filter(SidebarWidget.sidebar_id.like('footer-%')).first():
        w_col1 = SidebarWidget(
            sidebar_id='footer-1',
            widget_type='brand_logo',
            title='About Tek Club',
            sort_order=1
        )
        w_col1.set_config({
            'logo_url': '/static/img/tekclub_logo.svg',
            'description': 'Delivering cutting-edge enterprise IT solutions, cloud architectures, managed services, and scalable digital consulting for global industry leaders.',
            'phone': '+44 (0) 20 7946 0912',
            'email': 'solutions@tekclub.co.uk',
            'font_color': '#cbd5e1',
            'font_opacity': '100',
            'accent_color': '#ef3139',
            'accent_opacity': '100',
            'bg_color': '#ffffff',
            'bg_opacity': '0',
            'font_style': 'sans'
        })

        w_col2 = SidebarWidget(
            sidebar_id='footer-2',
            widget_type='menu_widget',
            title='IT Solutions',
            sort_order=1
        )
        w_col2.set_config({
            'menu_location': 'solutions',
            'font_color': '#cbd5e1',
            'font_opacity': '100',
            'accent_color': '#ef3139',
            'accent_opacity': '100',
            'bg_color': '#ffffff',
            'bg_opacity': '0',
            'font_style': 'sans'
        })

        w_col3 = SidebarWidget(
            sidebar_id='footer-3',
            widget_type='menu_widget',
            title='Quick Links',
            sort_order=1
        )
        w_col3.set_config({
            'menu_location': 'footer',
            'font_color': '#cbd5e1',
            'font_opacity': '100',
            'accent_color': '#ef3139',
            'accent_opacity': '100',
            'bg_color': '#ffffff',
            'bg_opacity': '0',
            'font_style': 'sans'
        })

        w_col4 = SidebarWidget(
            sidebar_id='footer-4',
            widget_type='newsletter',
            title='Newsletter',
            content='Subscribe to our weekly technology briefing covering cyber security, cloud strategies, and digital trends.',
            sort_order=1
        )
        w_col4.set_config({
            'font_color': '#cbd5e1',
            'font_opacity': '100',
            'accent_color': '#ef3139',
            'accent_opacity': '100',
            'bg_color': '#ffffff',
            'bg_opacity': '0',
            'font_style': 'sans'
        })
        db.session.add_all([w_col1, w_col2, w_col3, w_col4])

    # Seed default modules once upon initial installation
    if not SiteSetting.get('initial_modules_seeded'):
        from .utils.modules import get_default_config, MODULE_DEFINITIONS
        if not PageModule.query.filter_by(is_home=True).first():
            home_order = ['hero', 'features_strip', 'about', 'services', 'case_studies', 'posts', 'testimonials', 'trust_strip', 'contact_form']
            for idx, m_type in enumerate(home_order, 1):
                defn = MODULE_DEFINITIONS.get(m_type, {})
                m = PageModule(
                    is_home=True,
                    module_type=m_type,
                    title=defn.get('name', m_type.replace('_', ' ').title()),
                    placement='above',
                    sort_order=idx,
                    is_enabled=True
                )
                m.set_config(get_default_config(m_type))
                db.session.add(m)

        # Seed default modules for Contact page if none exist
        if contact_page and not PageModule.query.filter_by(page_id=contact_page.id).first():
            c_hero = PageModule(
                page_id=contact_page.id,
                module_type='hero',
                title='Hero Banner',
                placement='above',
                sort_order=1,
                is_enabled=True
            )
            c_hero_cfg = get_default_config('hero')
            c_hero_cfg['badge'] = 'Direct Contact'
            c_hero_cfg['headline'] = "Let's Discuss Your Architecture"
            c_hero_cfg['subtext'] = "Connect directly with our senior cloud engineers and solution architects."
            c_hero.set_config(c_hero_cfg)
            db.session.add(c_hero)

            c_cards = PageModule(
                page_id=contact_page.id,
                module_type='contact_cards',
                title='Contact Info Cards (3-Column)',
                placement='above',
                sort_order=2,
                is_enabled=True
            )
            c_cards.set_config(get_default_config('contact_cards'))
            db.session.add(c_cards)

            c_form = PageModule(
                page_id=contact_page.id,
                module_type='contact_form',
                title='Strategy Consultation Form',
                placement='below',
                sort_order=3,
                is_enabled=True
            )
            c_form.set_config(get_default_config('contact_form'))
            db.session.add(c_form)

        # Seed default modules for About page if none exist
        if about_page and not PageModule.query.filter_by(page_id=about_page.id).first():
            a_hero = PageModule(
                page_id=about_page.id,
                module_type='hero',
                title='Hero Banner',
                placement='above',
                sort_order=1,
                is_enabled=True
            )
            a_hero_cfg = get_default_config('hero')
            a_hero_cfg['badge'] = 'About Our Firm'
            a_hero_cfg['headline'] = "Enterprise Cloud & Digital Solutions"
            a_hero_cfg['subtext'] = "Delivering resilient containerized systems and managed infrastructure across the globe."
            a_hero.set_config(a_hero_cfg)
            db.session.add(a_hero)

            a_strip = PageModule(
                page_id=about_page.id,
                module_type='features_strip',
                title='Features Strip',
                placement='below',
                sort_order=2,
                is_enabled=True
            )
            a_strip.set_config(get_default_config('features_strip'))
            db.session.add(a_strip)

        SiteSetting.set('initial_modules_seeded', '1')

    # Ensure Quizmondo questions, pub leagues, categories, posts, and page modules are synchronized once per seed version
    try:
        from .models import QuizPack
        current_seed_ver = SiteSetting.get('quizmondo_seed_version')
        if current_seed_ver != '2026.10.26.v3' or QuizPack.query.count() < 15:
            from app.utils.quiz_seed import seed_quizmondo_full_environment
            seed_quizmondo_full_environment()
            SiteSetting.set('quizmondo_seed_version', '2026.10.26.v3')
    except Exception as e:
        app.logger.warning(f"Could not synchronize quizmondo seed environment: {e}")

    # Enforce default role hierarchy: trevorl is a standard player, primary admin is super_admin/admin
    try:
        trevor_user = User.query.filter(db.func.lower(User.username) == 'trevorl').first()
        if trevor_user and trevor_user.role != 'player':
            trevor_user.role = 'player'
        for u in User.query.all():
            if not u.role:
                u.role = 'player'
    except Exception:
        pass

    db.session.commit()
