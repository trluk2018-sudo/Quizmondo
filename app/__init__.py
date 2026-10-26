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

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(arena_bp)

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

        cols_leagues = [row[1] for row in db.session.execute(text("PRAGMA table_info(pub_leagues)")).fetchall()]
        if cols_leagues and 'teams_json' not in cols_leagues:
            db.session.execute(text("ALTER TABLE pub_leagues ADD COLUMN teams_json TEXT DEFAULT '[]'"))
            db.session.commit()

        cols_questions = [row[1] for row in db.session.execute(text("PRAGMA table_info(quiz_questions)")).fetchall()]
        if cols_questions:
            if 'status' not in cols_questions:
                db.session.execute(text("ALTER TABLE quiz_questions ADD COLUMN status VARCHAR(20) DEFAULT 'approved'"))
            if 'is_community' not in cols_questions:
                db.session.execute(text("ALTER TABLE quiz_questions ADD COLUMN is_community BOOLEAN DEFAULT 0"))
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

    # Ensure Quizmondo questions, pub leagues, categories, posts, and page modules are synchronized
    try:
        from app.utils.quiz_seed import seed_quizmondo_full_environment
        seed_quizmondo_full_environment()
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
