import json
from flask import Blueprint, render_template, request, abort, Response, current_app, flash, redirect, url_for, session
from ..models import db, Post, Page, Category, Media, MenuItem, SidebarWidget, SiteSetting, PageModule, PlayerProfile, ArenaMatch, FeaturedGame

public_bp = Blueprint('public', __name__)


def render_theme(template_name, **context):
    """Render template from active theme directory, falling back to quizhub arena default."""
    active_theme = SiteSetting.get('active_theme', 'quizhub')
    theme_template = f"themes/{active_theme}/{template_name}"
    try:
        return render_template(theme_template, active_theme=active_theme, **context)
    except Exception:
        # Fall back to quizhub default
        return render_template(f"themes/quizhub/{template_name}", active_theme='quizhub', **context)


@public_bp.app_context_processor
def inject_global_data():
    """Inject settings, navigation, player state, and sidebar widgets into all public & arena templates."""
    settings = SiteSetting.get_all()
    header_nav = MenuItem.query.filter_by(location='header', parent_id=None).order_by(MenuItem.sort_order.asc()).all()
    footer_nav = MenuItem.query.filter_by(location='footer', parent_id=None).order_by(MenuItem.sort_order.asc()).all()
    solutions_nav = MenuItem.query.filter_by(location='solutions', parent_id=None).order_by(MenuItem.sort_order.asc()).all()

    # Left, right and footer sidebars/widget areas
    left_widgets = SidebarWidget.query.filter_by(sidebar_id='sidebar-left', is_active=True).order_by(SidebarWidget.sort_order.asc()).all()
    right_widgets = SidebarWidget.query.filter_by(sidebar_id='sidebar-right', is_active=True).order_by(SidebarWidget.sort_order.asc()).all()
    footer_col1_widgets = SidebarWidget.query.filter_by(sidebar_id='footer-1', is_active=True).order_by(SidebarWidget.sort_order.asc()).all()
    footer_col2_widgets = SidebarWidget.query.filter_by(sidebar_id='footer-2', is_active=True).order_by(SidebarWidget.sort_order.asc()).all()
    footer_col3_widgets = SidebarWidget.query.filter_by(sidebar_id='footer-3', is_active=True).order_by(SidebarWidget.sort_order.asc()).all()
    footer_col4_widgets = SidebarWidget.query.filter_by(sidebar_id='footer-4', is_active=True).order_by(SidebarWidget.sort_order.asc()).all()
    has_footer_widgets = bool(footer_col1_widgets or footer_col2_widgets or footer_col3_widgets or footer_col4_widgets)

    recent_posts = Post.query.filter_by(status='publish').order_by(Post.created_at.desc()).limit(5).all()
    categories = Category.query.order_by(Category.name.asc()).all()

    current_player = None
    active_duel_turns_count = 0
    try:
        uid = session.get('user_id')
        pkey = session.get('qm_player_key')
        if uid:
            current_player = PlayerProfile.query.filter_by(user_id=uid).first()
        if not current_player and pkey:
            current_player = PlayerProfile.query.filter_by(session_key=pkey).first()
        if current_player:
            my_matches = ArenaMatch.query.filter(
                (ArenaMatch.player1_session == current_player.session_key) |
                (ArenaMatch.player2_session == current_player.session_key)
            ).filter(ArenaMatch.status.in_(['waiting', 'in_progress'])).all()
            active_duel_turns_count = sum(1 for m in my_matches if m.is_player_turn(current_player.session_key))
    except Exception:
        pass

    # Hero gallery slides; an empty list leaves the hero on its packaged image
    try:
        featured_games = FeaturedGame.query.filter_by(is_active=True).order_by(
            FeaturedGame.sort_order.asc(), FeaturedGame.id.asc()
        ).all()
    except Exception:
        featured_games = []

    return {
        'settings': settings,
        'featured_games': featured_games,
        'header_nav': header_nav,
        'footer_nav': footer_nav,
        'solutions_nav': solutions_nav,
        'left_widgets': left_widgets,
        'right_widgets': right_widgets,
        'footer_col1_widgets': footer_col1_widgets,
        'footer_col2_widgets': footer_col2_widgets,
        'footer_col3_widgets': footer_col3_widgets,
        'footer_col4_widgets': footer_col4_widgets,
        'has_footer_widgets': has_footer_widgets,
        'recent_posts': recent_posts,
        'categories': categories,
        'site_title': settings.get('site_title', 'SiteBuilder Express'),
        'site_tagline': settings.get('site_tagline', ''),
        'current_player': current_player,
        'active_duel_turns_count': active_duel_turns_count
    }


@public_bp.route('/')
def home():
    homepage_type = SiteSetting.get('homepage_type', 'posts')
    if homepage_type == 'page':
        page_id = SiteSetting.get('homepage_page_id')
        if page_id and str(page_id).isdigit():
            page = Page.query.filter_by(id=int(page_id), status='publish').first()
            if page:
                modules_above = PageModule.query.filter_by(page_id=page.id, placement='above', is_enabled=True).order_by(PageModule.sort_order.asc()).all()
                modules_below = PageModule.query.filter_by(page_id=page.id, placement='below', is_enabled=True).order_by(PageModule.sort_order.asc()).all()
                return render_theme('page.html', page=page, modules_above=modules_above, modules_below=modules_below)

    if homepage_type == 'blog_feed':
        page_num = request.args.get('page', 1, type=int)
        per_page = int(SiteSetting.get('posts_per_page', '10') or '10')
        pagination = Post.query.filter_by(status='publish').order_by(Post.created_at.desc()).paginate(page=page_num, per_page=per_page, error_out=False)
        return render_theme('posts.html', pagination=pagination)

    # Standard clean layout homepage with modular system for active theme
    active_theme = SiteSetting.get('active_theme', 'quizhub')
    home_modules = PageModule.query.filter_by(is_home=True, is_enabled=True, theme=active_theme).order_by(PageModule.sort_order.asc()).all()
    if not home_modules:
        # Fallback to un-themed, general, or legacy home modules
        home_modules = PageModule.query.filter(
            PageModule.is_home == True,
            PageModule.is_enabled == True,
            (PageModule.theme == active_theme) | (PageModule.theme == None) | (PageModule.theme == 'hisoft')
        ).order_by(PageModule.sort_order.asc()).all()

    has_modular_home = bool(home_modules or PageModule.query.filter_by(is_home=True).first() is not None or SiteSetting.get('initial_modules_seeded'))
    
    saved_modules_raw = SiteSetting.get(
        'home_modules_json',
        '["hero", "features_strip", "about", "services", "case_studies", "posts", "testimonials", "trust_strip", "contact"]'
    )
    try:
        active_modules = json.loads(saved_modules_raw)
    except Exception:
        active_modules = ['hero', 'features_strip', 'about', 'services', 'case_studies', 'posts', 'testimonials', 'trust_strip', 'contact']

    latest_posts = Post.query.filter_by(status='publish').order_by(Post.created_at.desc()).limit(6).all()
    return render_theme('home.html', home_modules=home_modules, has_modular_home=has_modular_home, active_modules=active_modules, latest_posts=latest_posts)


@public_bp.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)
    per_page = int(SiteSetting.get('posts_per_page', '10') or '10')
    # Pinned guides lead, in their own order, then everything else newest first.
    # Without this the is_pinned flag in the admin had no effect on the page at all.
    pagination = Post.query.filter_by(status='publish').order_by(
        Post.is_pinned.desc(), Post.pin_order.asc(), Post.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    return render_theme('posts.html', pagination=pagination)


@public_bp.route('/posts/<slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug, status='publish').first_or_404()
    post.view_count = (post.view_count or 0) + 1
    db.session.commit()
    modules_above = PageModule.query.filter_by(post_id=post.id, placement='above', is_enabled=True).order_by(PageModule.sort_order.asc()).all()
    modules_below = PageModule.query.filter_by(post_id=post.id, placement='below', is_enabled=True).order_by(PageModule.sort_order.asc()).all()
    return render_theme('post_detail.html', post=post, modules_above=modules_above, modules_below=modules_below)


@public_bp.route('/category/<slug>')
def category_detail(slug):
    cat = Category.query.filter_by(slug=slug).first_or_404()
    posts = Post.query.filter_by(category_id=cat.id, status='publish').order_by(Post.created_at.desc()).all()
    return render_theme('category.html', category=cat, posts=posts)


@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash('Thank you for your consultation request! Our engineering team will review it and reply promptly.', 'success')
        return redirect(url_for('public.contact'))

    page = Page.query.filter_by(slug='contact', status='publish').first()
    modules_above = []
    modules_below = []
    if page:
        modules_above = PageModule.query.filter_by(page_id=page.id, placement='above', is_enabled=True).order_by(PageModule.sort_order.asc()).all()
        modules_below = PageModule.query.filter_by(page_id=page.id, placement='below', is_enabled=True).order_by(PageModule.sort_order.asc()).all()
    return render_theme('contact.html', page=page, modules_above=modules_above, modules_below=modules_below)


@public_bp.route('/sitemap.xml')
def sitemap():
    posts = Post.query.filter_by(status='publish').all()
    pages = Page.query.filter_by(status='publish').all()
    base_url = current_app.config.get('APP_PUBLIC_URL', request.host_url.rstrip('/'))
    xml = render_template('public/sitemap.xml', posts=posts, pages=pages, base_url=base_url)
    return Response(xml, mimetype='application/xml')


@public_bp.route('/robots.txt')
def robots():
    base_url = current_app.config.get('APP_PUBLIC_URL', request.host_url.rstrip('/'))
    content = f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {base_url}/sitemap.xml\n"
    return Response(content, mimetype='text/plain')


# Dynamic page handler - catches /<slug>
@public_bp.route('/<slug>')
def page_view(slug):
    if slug in ('admin', 'static', 'posts', 'category'):
        abort(404)
    if slug == 'contact':
        return contact()
    page = Page.query.filter_by(slug=slug, status='publish').first_or_404()
    modules_above = PageModule.query.filter_by(page_id=page.id, placement='above', is_enabled=True).order_by(PageModule.sort_order.asc()).all()
    modules_below = PageModule.query.filter_by(page_id=page.id, placement='below', is_enabled=True).order_by(PageModule.sort_order.asc()).all()
    if page.template == 'contact':
        return render_theme('contact.html', page=page, modules_above=modules_above, modules_below=modules_below)
    elif page.template == 'full-width':
        return render_theme('page_fullwidth.html', page=page, modules_above=modules_above, modules_below=modules_below)
    return render_theme('page.html', page=page, modules_above=modules_above, modules_below=modules_below)
