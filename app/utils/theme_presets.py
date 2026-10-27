"""
Theme Presets Engine
Defines complete, authentic design presets, typography, brand assets,
and modular home content for the native Quizhub theme.
"""

THEME_PRESETS = {
    'quizhub': {
        'key': 'quizhub',
        'name': 'Quizmondo Cosmic Arena',
        'badge': 'Gaming & Trivia',
        'category': 'Interactive Quizzes, Brain Games & Tournaments',
        'description': 'Vibrant neon cyber-gaming arena with electric violet & cyan accents, daily trivia challenge cards, multiplayer competition leaderboards, and tournament prize pools.',
        'color': '#130924',
        'accent': '#8b5cf6',
        'settings': {
            'site_title': 'Quizmondo.com',
            'site_tagline': 'The Cosmic Arcade Trivia Arena & Multiplayer Brain Showdowns',
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
            'header_cta_text': 'Play Arena Duels',
            'header_cta_url': '/arena/',
            'footer_bg_color': '#090317',
            'footer_bg_opacity': '100',
            'footer_text_color': '#d8b4fe',
            'footer_text_opacity': '100',
            'footer_accent_color': '#06b6d4',
            'footer_accent_opacity': '100',
            'footer_logo': '/static/img/quizmondo_logo.svg',
            'footer_about_text': 'Quizmondo is the premier gamified brain arena featuring turn-based WhatsApp duels, weekly pub quiz leagues, community quiz decks, and prize vault rewards.',
            'footer_copyright': '© 2026 Quizmondo.com. All rights reserved.',
            'home_hero_title': 'The Cosmic Brain Arena: Challenge Friends & Climb the Leaderboards',
            'home_hero_subtitle': 'Battle head-to-head in turn-based trivia duels, join weekly live pub quiz leagues, and author community quiz decks. 100% free with WhatsApp invitations!',
            'home_hero_button_label': 'Play Daily Challenge ⚡',
            'home_hero_button_url': '/arena/',
            'layout_accent_color': '#8b5cf6',
            'footer_attribution': 'Images & Media courtesy of Pixabay / Freepik (Free Commercial License with Attribution)',
        },
        'menu_header': [
            ('Arena Home', '/'),
            ('Play Duels', '/arena/'),
            ('Trivia Decks', '/arena/packs'),
            ('Pub Leagues', '/arena/leagues'),
            ('Leaderboard', '/arena/leaderboard'),
            ('Quiz Studio', '/arena/create'),
            ('Articles', '/posts'),
        ],
        'menu_footer': [
            ('Arena Home', '/'),
            ('Play Duels', '/arena/'),
            ('Trivia Decks', '/arena/packs'),
            ('Pub Leagues', '/arena/leagues'),
            ('Leaderboard', '/arena/leaderboard'),
            ('Quiz Studio', '/arena/create'),
            ('Articles', '/posts'),
        ],
        'menu_solutions': [
            ('Daily Brain Challenge', '/#services'),
            ('Multiplayer eSports Leagues', '/#services'),
            ('Science & Tech Cups', '/#services'),
            ('Pop Culture & Cinema Faceoff', '/#services'),
            ('Corporate Team Quiz Arenas', '/#services'),
        ],
        'modules': [
            {
                'module_type': 'hero',
                'title': 'Arcade & Live Trivia Arena',
                'sort_order': 1,
                'config': {
                    'badge': 'Live Multiplayer Arena Active',
                    'headline': 'Battle Live in the Ultimate Trivia & Esports Brain Arena',
                    'subtext': 'Compete head-to-head in high-stakes live quizzes, win weekly cash tournament pools, and prove your intellectual supremacy on the global leaderboard.',
                    'primary_btn_text': 'Play Daily Challenge',
                    'primary_btn_url': '/#services',
                    'secondary_btn_text': 'Browse Tournaments',
                    'secondary_btn_url': '/contact',
                    'metric_val_1': '50K+',
                    'metric_lbl_1': 'Active Competitors',
                    'metric_val_2': '1,200+',
                    'metric_lbl_2': 'Live Daily Quizzes',
                    'metric_val_3': '£10,000',
                    'metric_lbl_3': 'Monthly Prize Pool',
                    'metric_val_4': '99.8%',
                    'metric_lbl_4': 'Anti-Cheat FairPlay',
                    'cert_text': 'Certified eSports Fair Play • Instant Secure Prize Payouts • Low Latency Engine',
                    'bg_style': 'deep-slate',
                    'font_color': '#f8fafc',
                    'font_opacity': '100',
                    'accent_color': '#8b5cf6',
                    'accent_opacity': '100'
                }
            },
            {
                'module_type': 'features_strip',
                'title': 'Live Gameplay & Tournament Highlights',
                'sort_order': 2,
                'config': {
                    'col1_title': 'Instant Live Matchmaking',
                    'col1_desc': 'Match against players of identical skill levels in under 5 seconds with zero server lag or question delay.',
                    'col2_title': 'Verified Cash Tournaments',
                    'col2_desc': 'Weekly and monthly prize leagues with transparent leaderboards and direct automated bank payouts.',
                    'col3_title': 'ProctorGuard Anti-Cheat',
                    'col3_desc': 'Proprietary biometric response telemetry ensuring genuine human play and zero automated bot cheating.',
                    'bg_style': 'slate-50',
                    'font_color': '#1e293b',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'about',
                'title': 'About Trivia Stadium & Fair-Play Rules',
                'sort_order': 3,
                'config': {
                    'kicker': 'The Gaming Revolution',
                    'headline': 'Where Intellectual Agility Meets eSports Competition',
                    'story_1': 'TriviaMatrix was created to elevate trivia and knowledge sports into an authentic competitive arena with broadcast-grade spectator modes and instant payouts.',
                    'story_2': 'Over 50,000 registered quiz gladiators battle daily across general knowledge, computer science, medicine, cinema, and world history.',
                    'check_1': 'Over 250,000 Peer-Reviewed Validated Trivia Questions',
                    'check_2': 'Sub-15ms Real-Time Multiplayer WebSocket Infrastructure',
                    'check_3': 'Global ELO Ranking System with Divisional Tiers',
                    'year_established': '2023',
                    'established_label': 'Years Powering Competitive Gaming',
                    'bg_style': 'white',
                    'font_color': '#0f0728',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'services',
                'title': 'Quiz Disciplines & Game Modes Grid',
                'sort_order': 4,
                'config': {
                    'kicker': 'Game Modes',
                    'headline': 'Choose Your Battleground: 6 Intense Competition Formats',
                    'subhead': 'From lightning 60-second speed rounds to marathon tournament championships.',
                    's1_title': 'Daily Speed Blitz',
                    's1_desc': '10 rapid-fire questions in 60 seconds. High multipliers for speed streaks with daily leaderboard trophies.',
                    's2_title': 'Live Weekend Tournaments',
                    's2_desc': 'Single-elimination bracket tournaments with £2,500 weekend cash pools and live twitch spectator streams.',
                    's3_title': 'Science & Technology Cup',
                    's3_desc': 'Hardcore trivia covering quantum physics, machine learning, aerospace, and software architecture.',
                    's4_title': 'Pop Culture & Cinema League',
                    's4_desc': 'Deep trivia covering cinematic universes, 80s & 90s music, gaming lore, and comic book history.',
                    's5_title': '1v1 High-Roller Duels',
                    's5_desc': 'Wager points against friends or rivals in private duel rooms with custom category picks and timers.',
                    's6_title': 'Corporate Team Arenas',
                    's6_desc': 'Gamified company trivia events and team-building tournaments with custom corporate branding.',
                    'bg_style': 'slate-50',
                    'font_color': '#0f0728',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'case_studies',
                'title': 'Tournament Hall of Fame & Champions',
                'sort_order': 5,
                'config': {
                    'kicker': 'Hall of Fame',
                    'headline': 'Legendary Champions & Tournament Records',
                    'c1_tag': 'UK Championship',
                    'c1_title': 'Winning the £5,000 Summer Brain Invitational',
                    'c1_desc': 'How player "NeuralViper" answered 48 out of 50 speed questions in 42 seconds to claim the trophy.',
                    'c2_tag': 'Corporate League',
                    'c2_title': 'Enterprise Trivia Championship with 1,500 Live Employees',
                    'c2_desc': 'Global tech company boosted remote employee engagement scores by 74% with weekly live team arenas.',
                    'c3_tag': 'Universities',
                    'c3_title': 'Inter-Collegiate Knowledge Olympiad',
                    'c3_desc': '32 universities competed in an automated 4-week league streamed to over 40,000 live spectators.',
                    'bg_style': 'white',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'posts',
                'title': 'Arena Dispatches & Trivia Tactics',
                'sort_order': 6,
                'config': {
                    'kicker': 'Arena News',
                    'headline': 'Tournament Announcements, Patch Notes & Strategy Guides',
                    'subhead': 'Stay up to date with new question drops, season resets, and prize pool expansions.',
                    'bg_style': 'slate-50',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'testimonials',
                'title': 'Player Reviews & Champion Quotes',
                'sort_order': 7,
                'config': {
                    'kicker': 'Player Feedback',
                    'headline': 'What Competitive Quiz Enthusiasts Are Saying',
                    't1_quote': 'The thrill of the final countdown in the Sunday Major is unmatched. The payouts are instant and the questions are genuinely brilliant.',
                    't1_name': 'Liam Davies',
                    't1_role': 'Grandmaster Division Player, Manchester',
                    't2_quote': 'We host all our company town hall trivia sessions on TriviaMatrix. Flawless latency and our staff absolutely look forward to it all week.',
                    't2_name': 'Chloe Martinez',
                    't2_role': 'Head of People, FinScale Cloud',
                    't3_quote': 'Finally a trivia platform with zero bots and serious anti-cheat. The ranking system is fair and immensely addictive.',
                    't3_name': 'Oliver Thorne',
                    't3_role': 'University Quiz Team Captain',
                    'bg_style': 'white',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'trust_strip',
                'title': 'Fair-Play & Anti-Cheat Certification Strip',
                'sort_order': 8,
                'config': {
                    'label': 'Trusted by Competitive Esports Clubs & Certified Fair Play',
                    'b1_title': 'Instant Payouts',
                    'b1_sub': 'Direct Bank & Stripe Verified',
                    'b2_title': 'Anti-Cheat AI',
                    'b2_sub': 'Zero Bot Tolerance',
                    'b3_title': 'Sub-15ms Latency',
                    'b3_sub': 'Real-Time WebSockets',
                    'b4_title': 'FairPlay 2026',
                    'b4_sub': 'Certified eSports Rules',
                    'bg_style': 'slate-50',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'contact_form',
                'title': 'Host a League or Tournament Desk',
                'sort_order': 9,
                'config': {
                    'kicker': 'Host an Event',
                    'headline': 'Host a Private Tournament or Corporate Trivia Arena',
                    'subhead': 'Inquire about branded quiz leagues, custom question packs, and private enterprise servers.',
                    'submit_btn_text': 'Request Tournament Hosting',
                    'bg_style': 'white',
                    'accent_color': '#8b5cf6'
                }
            }
        ],
        'sidebar_widgets': {
            'recent_posts_title': 'Arena Match Logs',
            'categories_title': 'Battle Categories',
        },
        'pages': [
            {
                'slug': 'about',
                'title': 'About TriviaMatrix Arena',
                'excerpt': 'The premier live multiplayer brain gaming, esports trivia arena, and competitive knowledge championships.',
                'template': 'default',
                'content': '<p>TriviaMatrix Arena is the ultimate digital stadium for competitive brain gaming, live multiplayer trivia tournaments, and global knowledge showdowns.</p><h2>The Arena Engine</h2><p>Our real-time matchmaking engine pairs competitors across 50+ specialized categories, from quantum physics to cinematic history, delivering millisecond-accurate buzzer response and anti-cheat verification.</p><h3>Arena Highlights</h3><ul><li>Live Multiplayer Daily Cups with Real-Time Leaderboards</li><li>Ranked Elo Matchmaking &amp; Verified Grandmaster Divisions</li><li>Adaptive Difficulty Algorithms Tailored to Player Elo</li><li>Cryptographically Signed Tournament Cups &amp; Cash Prizes</li></ul>'
            },
            {
                'slug': 'contact',
                'title': 'Arena Match Operations & Tournament Support',
                'excerpt': 'Inquire about tournament sponsorships, corporate team leagues, or arena account support.',
                'template': 'contact',
                'content': '<p>Contact the TriviaMatrix Arena Match Directors for tournament schedule inquiries, custom corporate trivia leagues, or competitive referee support.</p>'
            }
        ],
        'categories': [
            {'name': 'Tournament Announcements', 'slug': 'tournament-announcements', 'description': 'Official schedules, prize pool releases, and bracket updates.'},
            {'name': 'Pro Trivia Tactics', 'slug': 'pro-trivia-tactics', 'description': 'Speed-round cognitive techniques, buzzer optimization, and memory mnemonics.'},
            {'name': 'Community Spotlights', 'slug': 'community-spotlights', 'description': 'Profiles of arena grandmasters, record streaks, and trivia legends.'}
        ],
        'posts': [
            {
                'title': 'World Trivia Championship 2026: Arena Registration Now Open',
                'slug': 'world-trivia-championship-2026-registration',
                'excerpt': 'Compete against 10,000 global players across 10 qualifier stages for the $50,000 championship trophy.',
                'featured_image': '/static/img/triviamatrix_post1.svg',
                'category_slug': 'tournament-announcements',
                'content': '<p>The annual World Trivia Championship kicks off next month in the TriviaMatrix Arena. Featuring double-elimination brackets and speed-buzzer showdowns, this year’s tournament spans 8 core disciplines.</p><p>Qualifiers will stream live to hundreds of thousands of spectators with live studio commentary and real-time interactive audience polls.</p>'
            },
            {
                'title': 'Mastering Speed-Round Tactics: How Top Arena Players Think Under 5 Seconds',
                'slug': 'mastering-speed-round-tactics',
                'excerpt': 'Cognitive priming and rapid deduction strategies used by top-ranked Grandmasters.',
                'featured_image': '/static/img/triviamatrix_post2.svg',
                'category_slug': 'pro-trivia-tactics',
                'content': '<p>In high-stakes arena trivia, knowledge alone is only half the equation. Response latency under 4.5 seconds determines who takes the buzzer lead.</p><p>Grandmasters utilize keyword scanning, predictive phonetics, and associative mnemonics to isolate the correct option before the question prompt finishes animating.</p>'
            },
            {
                'title': 'Community Spotlight: Inside the 48-Win Streak of Matrix Grandmaster \'VortexMind\'',
                'slug': 'community-spotlight-vortexmind-streak',
                'excerpt': 'An exclusive interview with the highest Elo player in TriviaMatrix Arena history.',
                'featured_image': '/static/img/triviamatrix_post3.svg',
                'category_slug': 'community-spotlights',
                'content': '<p>VortexMind has captivated the esports trivia community with an unprecedented 48 consecutive tournament victories. In this candid profile, they break down their daily memory training routines, favorite question categories, and mental resilience under pressure.</p>'
            }
        ]
    },
}


def apply_theme_preset(theme_key):
    """
    Applies the full design preset, colors, header/footer configuration,
    modular homepage sections, pages, posts, and widgets for the chosen theme.
    """
    from ..models import db, SiteSetting, PageModule, SidebarWidget, MenuItem, Page, Post, Category, User

    preset = THEME_PRESETS.get(theme_key)
    if not preset:
        return False, f"Unknown theme preset: {theme_key}"

    # 1. Update Core Site Settings
    SiteSetting.set('active_theme', theme_key)
    for k, v in preset['settings'].items():
        SiteSetting.set(k, v)

    # 2. Overwrite Homepage Modules for this Theme
    # Cleanly remove all existing homepage modules
    PageModule.query.filter(PageModule.is_home == True).delete()

    # Also clean any stale modules attached to standard pages (about, contact)
    default_page_ids = [p.id for p in Page.query.filter(Page.slug.in_(['about', 'contact'])).all()]
    if default_page_ids:
        PageModule.query.filter(PageModule.page_id.in_(default_page_ids)).delete()

    # Recreate homepage modules matching theme preset
    for m_data in preset['modules']:
        m = PageModule(
            is_home=True,
            theme=theme_key,
            module_type=m_data['module_type'],
            title=m_data['title'],
            placement='above',
            sort_order=m_data['sort_order'],
            is_enabled=True
        )
        m.set_config(m_data['config'])
        db.session.add(m)

    # 3. Update / Seed Footer Column Widgets
    SidebarWidget.query.filter(SidebarWidget.sidebar_id.like('footer-%')).delete()

    # Footer Col 1: Brand Logo Widget
    w1 = SidebarWidget(
        sidebar_id='footer-1',
        widget_type='brand_logo',
        title=f"About {preset['settings']['site_title']}",
        sort_order=1
    )
    w1.set_config({
        'logo_url': preset['settings'].get('footer_logo') or preset['settings']['site_logo'],
        'description': preset['settings']['footer_about_text'],
        'phone': SiteSetting.get('contact_phone', '+44 (0) 20 7946 0912'),
        'email': SiteSetting.get('contact_email', 'solutions@tekclub.co.uk'),
        'font_color': preset['settings']['footer_text_color'],
        'font_opacity': '100',
        'accent_color': preset['settings']['footer_accent_color'],
        'accent_opacity': '100',
        'bg_color': '#ffffff',
        'bg_opacity': '0',
        'font_style': preset['settings'].get('header_font_style', 'sans')
    })

    # Footer Col 2: Solutions / Practice Areas Menu Widget
    w2 = SidebarWidget(
        sidebar_id='footer-2',
        widget_type='menu_widget',
        title='Practice Areas' if theme_key == 'hisoft' else ('Nutrition Focus' if theme_key == 'nest' else ('Disciplines & Modes' if theme_key == 'quizhub' else ('Training Programs' if theme_key == 'gym' else 'Academic Tracks'))),
        sort_order=1
    )
    w2.set_config({
        'menu_location': 'solutions',
        'font_color': preset['settings']['footer_text_color'],
        'font_opacity': '100',
        'accent_color': preset['settings']['footer_accent_color'],
        'accent_opacity': '100',
        'bg_color': '#ffffff',
        'bg_opacity': '0',
        'font_style': 'sans'
    })

    # Footer Col 3: Quick Links Menu Widget
    w3 = SidebarWidget(
        sidebar_id='footer-3',
        widget_type='menu_widget',
        title='Quick Links',
        sort_order=1
    )
    w3.set_config({
        'menu_location': 'footer',
        'font_color': preset['settings']['footer_text_color'],
        'font_opacity': '100',
        'accent_color': preset['settings']['footer_accent_color'],
        'accent_opacity': '100',
        'bg_color': '#ffffff',
        'bg_opacity': '0',
        'font_style': 'sans'
    })

    # Footer Col 4: Newsletter Widget
    w4 = SidebarWidget(
        sidebar_id='footer-4',
        widget_type='newsletter',
        title='Newsletter',
        content=f"Subscribe to our weekly briefing for {preset['settings']['site_title']} announcements and updates.",
        sort_order=1
    )
    w4.set_config({
        'font_color': preset['settings']['footer_text_color'],
        'font_opacity': '100',
        'accent_color': preset['settings']['footer_accent_color'],
        'accent_opacity': '100',
        'bg_color': '#ffffff',
        'bg_opacity': '0',
        'font_style': 'sans'
    })
    db.session.add_all([w1, w2, w3, w4])

    # 4. Update or Create Standard Pages (About, Contact) for this theme
    if 'pages' in preset:
        for p_data in preset['pages']:
            existing_page = Page.query.filter_by(slug=p_data['slug']).first()
            if existing_page:
                existing_page.title = p_data['title']
                existing_page.content = p_data['content']
                existing_page.excerpt = p_data.get('excerpt', '')
                if 'template' in p_data:
                    existing_page.template = p_data['template']
            else:
                new_page = Page(
                    title=p_data['title'],
                    slug=p_data['slug'],
                    content=p_data['content'],
                    excerpt=p_data.get('excerpt', ''),
                    template=p_data.get('template', 'default'),
                    status='publish'
                )
                db.session.add(new_page)

    # 5. Update Categories & Replace Blog Posts for this Theme
    cat_map = {}
    if 'categories' in preset:
        for c_data in preset['categories']:
            cat = Category.query.filter_by(slug=c_data['slug']).first()
            if not cat:
                cat = Category(
                    name=c_data['name'],
                    slug=c_data['slug'],
                    description=c_data.get('description', '')
                )
                db.session.add(cat)
                db.session.flush()
            cat_map[c_data['slug']] = cat.id

    first_user = User.query.first()
    author_id = first_user.id if first_user else None

    if 'posts' in preset:
        # Cleanly replace sample posts with active theme's authentic articles
        Post.query.delete()
        for post_data in preset['posts']:
            cat_id = cat_map.get(post_data.get('category_slug'))
            new_post = Post(
                title=post_data['title'],
                slug=post_data['slug'],
                content=post_data['content'],
                excerpt=post_data.get('excerpt', ''),
                featured_image=post_data.get('featured_image', ''),
                category_id=cat_id,
                author_id=author_id,
                status='publish'
            )
            db.session.add(new_post)

    # 6. Update Sidebar Right Widget Titles to Match Theme Vertical
    sw_cfg = preset.get('sidebar_widgets', {})
    recent_widget = SidebarWidget.query.filter_by(sidebar_id='sidebar-right', widget_type='recent_posts').first()
    if recent_widget and sw_cfg.get('recent_posts_title'):
        recent_widget.title = sw_cfg['recent_posts_title']
    cat_widget = SidebarWidget.query.filter_by(sidebar_id='sidebar-right', widget_type='categories').first()
    if cat_widget and sw_cfg.get('categories_title'):
        cat_widget.title = sw_cfg['categories_title']

    # 7. Update Solutions Submenu Items to match Theme Vertical
    preset_sol = preset.get('menu_solutions', [])
    if preset_sol:
        sol_items = MenuItem.query.filter_by(location='solutions', parent_id=None)\
            .order_by(MenuItem.sort_order.asc(), MenuItem.id.asc()).all()
        for idx, (lbl, url) in enumerate(preset_sol):
            if idx < len(sol_items):
                sol_items[idx].title = lbl
                sol_items[idx].url = url
                sol_items[idx].sort_order = idx + 1
            else:
                db.session.add(MenuItem(
                    title=lbl,
                    url=url,
                    location='solutions',
                    sort_order=idx + 1
                ))
        if len(sol_items) > len(preset_sol):
            for extra in sol_items[len(preset_sol):]:
                db.session.delete(extra)

    # 8. Update Header Menu to match Theme Vertical (Preserving user-added submenus)
    preset_header = preset.get('menu_header', [])
    if preset_header:
        header_roots = MenuItem.query.filter_by(location='header', parent_id=None)\
            .order_by(MenuItem.sort_order.asc(), MenuItem.id.asc()).all()
        for idx, (lbl, url) in enumerate(preset_header):
            if idx < len(header_roots):
                header_roots[idx].title = lbl
                header_roots[idx].url = url
                header_roots[idx].sort_order = idx + 1
            else:
                db.session.add(MenuItem(
                    title=lbl,
                    url=url,
                    location='header',
                    sort_order=idx + 1
                ))

    # 9. Update Footer Menu to match Theme Vertical
    preset_footer = preset.get('menu_footer', [])
    if preset_footer:
        footer_roots = MenuItem.query.filter_by(location='footer', parent_id=None)\
            .order_by(MenuItem.sort_order.asc(), MenuItem.id.asc()).all()
        for idx, (lbl, url) in enumerate(preset_footer):
            if idx < len(footer_roots):
                footer_roots[idx].title = lbl
                footer_roots[idx].url = url
                footer_roots[idx].sort_order = idx + 1
            else:
                db.session.add(MenuItem(
                    title=lbl,
                    url=url,
                    location='footer',
                    sort_order=idx + 1
                ))
        if len(footer_roots) > len(preset_footer):
            for extra in footer_roots[len(preset_footer):]:
                db.session.delete(extra)

    db.session.commit()
    return True, f"Theme successfully switched to {preset['name']}! Preset layout, colors, pages, posts, and modules have been imported."
