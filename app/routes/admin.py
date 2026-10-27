import os
import json
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from werkzeug.utils import secure_filename
from ..models import db, User, Post, Category, Page, Media, MenuItem, SidebarWidget, SiteSetting, PageModule, slugify, QuizQuestion, QuizPack, PlayerProfile, ArenaMatch, ArenaRound, PubLeague
from ..utils.modules import get_default_config, get_module_definition, MODULE_DEFINITIONS
from .auth import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
def require_admin_role():
    """Strict security lockdown: the entire Quizmondo Control Centre backend is strictly for administrators only."""
    if not session.get('user_id'):
        return redirect(url_for('auth.login', next=request.url))
    if session.get('user_role') not in ('admin', 'super_admin'):
        flash('Quizmondo Control Centre backend is restricted to administrators only.', 'error')
        return redirect(url_for('public.home'))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# -------------------------------------------------------------------------
# Dashboard
# -------------------------------------------------------------------------
@admin_bp.route('/')
@login_required
def dashboard():
    post_count = Post.query.count()
    page_count = Page.query.count()
    media_count = Media.query.count()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    recent_pages = Page.query.order_by(Page.updated_at.desc()).limit(5).all()

    questions_count = QuizQuestion.query.count()
    duels_count = ArenaMatch.query.count()
    players_count = PlayerProfile.query.count()
    leagues_count = PubLeague.query.count()
    recent_duels = ArenaMatch.query.order_by(ArenaMatch.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        post_count=post_count,
        page_count=page_count,
        media_count=media_count,
        recent_posts=recent_posts,
        recent_pages=recent_pages,
        questions_count=questions_count,
        duels_count=duels_count,
        players_count=players_count,
        leagues_count=leagues_count,
        recent_duels=recent_duels
    )


# -------------------------------------------------------------------------
# Posts
# -------------------------------------------------------------------------
@admin_bp.route('/posts')
@login_required
def posts():
    status = request.args.get('status')
    query = Post.query
    if status in ('publish', 'draft'):
        query = query.filter_by(status=status)
    all_posts = query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=all_posts, current_status=status)


@admin_bp.route('/posts/new', methods=['GET', 'POST'])
@login_required
def post_new():
    categories = Category.query.order_by(Category.name.asc()).all()
    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        if not title:
            flash('Post title is required.', 'error')
            return redirect(url_for('admin.post_new'))

        slug = slugify(request.form.get('slug') or title)
        base_slug = slug
        counter = 1
        while Post.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        post = Post(
            title=title,
            slug=slug,
            content=request.form.get('content') or '',
            excerpt=request.form.get('excerpt') or '',
            featured_image=request.form.get('featured_image') or '',
            status=request.form.get('status', 'publish'),
            category_id=int(request.form.get('category_id')) if request.form.get('category_id') else None,
            is_pinned=bool(request.form.get('is_pinned')),
            meta_title=request.form.get('meta_title', '').strip(),
            meta_description=request.form.get('meta_description', '').strip(),
            meta_keywords=request.form.get('meta_keywords', '').strip(),
            canonical_url=request.form.get('canonical_url', '').strip(),
            og_image=request.form.get('og_image', '').strip(),
            no_index=bool(request.form.get('no_index'))
        )
        db.session.add(post)
        db.session.commit()

        # Instantiate any modules added before saving
        staged_raw = request.form.get('staged_modules_json', '[]')
        try:
            staged_list = json.loads(staged_raw)
        except Exception:
            staged_list = []

        for idx, item in enumerate(staged_list):
            m_type = item.get('module_type')
            if m_type in MODULE_DEFINITIONS:
                default_cfg = get_default_config(m_type)
                pm = PageModule(
                    post_id=post.id,
                    module_type=m_type,
                    title=item.get('title') or MODULE_DEFINITIONS[m_type]['name'],
                    placement=item.get('placement', 'above'),
                    sort_order=idx + 1,
                    is_enabled=bool(item.get('is_enabled', True))
                )
                pm.set_config(default_cfg)
                db.session.add(pm)
        if staged_list:
            db.session.commit()

        flash('Post created successfully with configured content modules.', 'success')
        return redirect(url_for('admin.post_edit', post_id=post.id))

    return render_template(
        'admin/post_edit.html',
        post=None,
        categories=categories,
        modules_above=[],
        modules_below=[],
        available_modules=MODULE_DEFINITIONS
    )


@admin_bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    categories = Category.query.order_by(Category.name.asc()).all()

    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        if not title:
            flash('Post title is required.', 'error')
            return redirect(url_for('admin.post_edit', post_id=post.id))

        new_slug = slugify(request.form.get('slug') or title)
        if new_slug != post.slug:
            base_slug = new_slug
            counter = 1
            while Post.query.filter(Post.slug == new_slug, Post.id != post.id).first():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = new_slug

        post.title = title
        post.content = request.form.get('content') or ''
        post.excerpt = request.form.get('excerpt') or ''
        post.featured_image = request.form.get('featured_image') or ''
        post.status = request.form.get('status', 'publish')
        post.category_id = int(request.form.get('category_id')) if request.form.get('category_id') else None
        post.is_pinned = bool(request.form.get('is_pinned'))
        post.meta_title = request.form.get('meta_title', '').strip()
        post.meta_description = request.form.get('meta_description', '').strip()
        post.meta_keywords = request.form.get('meta_keywords', '').strip()
        post.canonical_url = request.form.get('canonical_url', '').strip()
        post.og_image = request.form.get('og_image', '').strip()
        post.no_index = bool(request.form.get('no_index'))
        post.updated_at = datetime.utcnow()

        # Update module ordering, enabled states, and process deletions for post
        deleted_ids_raw = request.form.get('deleted_module_ids', '')
        deleted_ids = set([int(i.strip()) for i in deleted_ids_raw.split(',') if i.strip().isdigit()])

        # Process newly staged modules created in the post editor
        staged_raw = request.form.get('staged_modules_json', '[]')
        staged_created = {}
        try:
            staged_list = json.loads(staged_raw)
            for sm in staged_list:
                temp_id = sm.get('temp_id')
                sm_type = sm.get('module_type', 'rich_text')
                sm_title = sm.get('title') or sm_type.replace('_', ' ').title()
                sm_placement = sm.get('placement', 'above')
                sm_enabled = bool(sm.get('is_enabled', True))
                pm = PageModule(
                    post_id=post.id,
                    module_type=sm_type,
                    title=sm_title,
                    placement=sm_placement,
                    sort_order=999,
                    is_enabled=sm_enabled
                )
                pm.set_config(get_default_config(sm_type))
                db.session.add(pm)
                db.session.flush()
                if temp_id:
                    staged_created[temp_id] = pm
                else:
                    staged_created[f"staged_{sm_type}"] = pm
        except Exception:
            pass

        module_order_raw = request.form.get('module_order', '')
        ordered_tokens = [i.strip() for i in module_order_raw.split(',') if i.strip()]
        enabled_ids = set([int(i) for i in request.form.getlist('enabled_modules') if i.isdigit()])

        all_post_mods = PageModule.query.filter_by(post_id=post.id).all()
        id_map = {m.id: m for m in all_post_mods if m.id not in [p.id for p in staged_created.values()]}

        curr_order = 1
        handled_staged = set()
        if ordered_tokens:
            for token in ordered_tokens:
                if token.isdigit():
                    mid = int(token)
                    if mid in id_map:
                        if mid in deleted_ids:
                            db.session.delete(id_map[mid])
                        else:
                            id_map[mid].sort_order = curr_order
                            id_map[mid].is_enabled = (mid in enabled_ids)
                            curr_order += 1
                elif token in staged_created:
                    staged_mod = staged_created[token]
                    staged_mod.sort_order = curr_order
                    handled_staged.add(token)
                    curr_order += 1

            for mid, m in id_map.items():
                if mid in deleted_ids or mid not in [int(t) for t in ordered_tokens if t.isdigit()]:
                    db.session.delete(m)
        else:
            for mid, m in id_map.items():
                if mid in deleted_ids:
                    db.session.delete(m)
                else:
                    m.is_enabled = (mid in enabled_ids)

        for tid, sm in staged_created.items():
            if tid not in handled_staged:
                sm.sort_order = curr_order
                curr_order += 1

        db.session.commit()
        flash('Post updated successfully.', 'success')
        return redirect(url_for('admin.post_edit', post_id=post.id))

    modules_above = PageModule.query.filter_by(post_id=post.id, placement='above').order_by(PageModule.sort_order.asc()).all()
    modules_below = PageModule.query.filter_by(post_id=post.id, placement='below').order_by(PageModule.sort_order.asc()).all()

    return render_template(
        'admin/post_edit.html',
        post=post,
        categories=categories,
        modules_above=modules_above,
        modules_below=modules_below,
        available_modules=MODULE_DEFINITIONS
    )


@admin_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'info')
    return redirect(url_for('admin.posts'))


# -------------------------------------------------------------------------
# Pages
# -------------------------------------------------------------------------
@admin_bp.route('/pages')
@login_required
def pages():
    all_pages = Page.query.order_by(Page.sort_order.asc(), Page.title.asc()).all()
    return render_template('admin/pages.html', pages=all_pages)


@admin_bp.route('/pages/new', methods=['GET', 'POST'])
@login_required
def page_new():
    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        if not title:
            flash('Page title is required.', 'error')
            return redirect(url_for('admin.page_new'))

        slug = slugify(request.form.get('slug') or title)
        base_slug = slug
        counter = 1
        while Page.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        page = Page(
            title=title,
            slug=slug,
            content=request.form.get('content') or '',
            excerpt=request.form.get('excerpt') or '',
            template=request.form.get('template', 'default'),
            status=request.form.get('status', 'publish'),
            sort_order=int(request.form.get('sort_order') or 0),
            show_in_nav=bool(request.form.get('show_in_nav', True)),
            meta_title=request.form.get('meta_title', '').strip(),
            meta_description=request.form.get('meta_description', '').strip(),
            meta_keywords=request.form.get('meta_keywords', '').strip(),
            canonical_url=request.form.get('canonical_url', '').strip(),
            og_image=request.form.get('og_image', '').strip(),
            no_index=bool(request.form.get('no_index'))
        )
        db.session.add(page)
        db.session.commit()

        # Instantiate any modules added before saving
        staged_raw = request.form.get('staged_modules_json', '[]')
        try:
            staged_list = json.loads(staged_raw)
        except Exception:
            staged_list = []

        for idx, item in enumerate(staged_list):
            m_type = item.get('module_type')
            if m_type in MODULE_DEFINITIONS:
                default_cfg = get_default_config(m_type)
                pm = PageModule(
                    page_id=page.id,
                    module_type=m_type,
                    title=item.get('title') or MODULE_DEFINITIONS[m_type]['name'],
                    placement=item.get('placement', 'above'),
                    sort_order=idx + 1,
                    is_enabled=bool(item.get('is_enabled', True))
                )
                pm.set_config(default_cfg)
                db.session.add(pm)
        if staged_list:
            db.session.commit()

        flash('Page created successfully with configured content modules.', 'success')
        return redirect(url_for('admin.page_edit', page_id=page.id))

    return render_template(
        'admin/page_edit.html',
        page=None,
        modules_above=[],
        modules_below=[],
        available_modules=MODULE_DEFINITIONS
    )


@admin_bp.route('/pages/<int:page_id>/edit', methods=['GET', 'POST'])
@login_required
def page_edit(page_id):
    page = Page.query.get_or_404(page_id)

    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        if not title:
            flash('Page title is required.', 'error')
            return redirect(url_for('admin.page_edit', page_id=page.id))

        new_slug = slugify(request.form.get('slug') or title)
        if new_slug != page.slug:
            base_slug = new_slug
            counter = 1
            while Page.query.filter(Page.slug == new_slug, Page.id != page.id).first():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            page.slug = new_slug

        page.title = title
        page.content = request.form.get('content') or ''
        page.excerpt = request.form.get('excerpt') or ''
        page.template = request.form.get('template', 'default')
        page.status = request.form.get('status', 'publish')
        page.sort_order = int(request.form.get('sort_order') or 0)
        page.show_in_nav = bool(request.form.get('show_in_nav'))
        page.meta_title = request.form.get('meta_title', '').strip()
        page.meta_description = request.form.get('meta_description', '').strip()
        page.meta_keywords = request.form.get('meta_keywords', '').strip()
        page.canonical_url = request.form.get('canonical_url', '').strip()
        page.og_image = request.form.get('og_image', '').strip()
        page.no_index = bool(request.form.get('no_index'))
        page.updated_at = datetime.utcnow()

        # Update module ordering, enabled states, and process deletions
        deleted_ids_raw = request.form.get('deleted_module_ids', '')
        deleted_ids = set([int(i.strip()) for i in deleted_ids_raw.split(',') if i.strip().isdigit()])

        # Process newly staged modules created in the editor
        staged_raw = request.form.get('staged_modules_json', '[]')
        staged_created = {}
        try:
            staged_list = json.loads(staged_raw)
            for sm in staged_list:
                temp_id = sm.get('temp_id')
                sm_type = sm.get('module_type', 'rich_text')
                sm_title = sm.get('title') or sm_type.replace('_', ' ').title()
                sm_placement = sm.get('placement', 'above')
                sm_enabled = bool(sm.get('is_enabled', True))
                pm = PageModule(
                    page_id=page.id,
                    module_type=sm_type,
                    title=sm_title,
                    placement=sm_placement,
                    sort_order=999,
                    is_enabled=sm_enabled
                )
                pm.set_config(get_default_config(sm_type))
                db.session.add(pm)
                db.session.flush()
                if temp_id:
                    staged_created[temp_id] = pm
                else:
                    staged_created[f"staged_{sm_type}"] = pm
        except Exception:
            pass

        module_order_raw = request.form.get('module_order', '')
        ordered_tokens = [i.strip() for i in module_order_raw.split(',') if i.strip()]
        enabled_ids = set([int(i) for i in request.form.getlist('enabled_modules') if i.isdigit()])

        all_page_mods = PageModule.query.filter_by(page_id=page.id).all()
        id_map = {m.id: m for m in all_page_mods if m.id not in [p.id for p in staged_created.values()]}

        curr_order = 1
        handled_staged = set()
        if ordered_tokens:
            for token in ordered_tokens:
                if token.isdigit():
                    mid = int(token)
                    if mid in id_map:
                        if mid in deleted_ids:
                            db.session.delete(id_map[mid])
                        else:
                            id_map[mid].sort_order = curr_order
                            id_map[mid].is_enabled = (mid in enabled_ids)
                            curr_order += 1
                elif token in staged_created:
                    staged_mod = staged_created[token]
                    staged_mod.sort_order = curr_order
                    handled_staged.add(token)
                    curr_order += 1

            for mid, m in id_map.items():
                if mid in deleted_ids or mid not in [int(t) for t in ordered_tokens if t.isdigit()]:
                    db.session.delete(m)
        else:
            for mid, m in id_map.items():
                if mid in deleted_ids:
                    db.session.delete(m)
                else:
                    m.is_enabled = (mid in enabled_ids)

        for tid, sm in staged_created.items():
            if tid not in handled_staged:
                sm.sort_order = curr_order
                curr_order += 1

        db.session.commit()
        flash('Page updated successfully.', 'success')
        return redirect(url_for('admin.page_edit', page_id=page.id))

    modules_above = PageModule.query.filter_by(page_id=page.id, placement='above').order_by(PageModule.sort_order.asc()).all()
    modules_below = PageModule.query.filter_by(page_id=page.id, placement='below').order_by(PageModule.sort_order.asc()).all()

    return render_template(
        'admin/page_edit.html',
        page=page,
        modules_above=modules_above,
        modules_below=modules_below,
        available_modules=MODULE_DEFINITIONS
    )


@admin_bp.route('/pages/<int:page_id>/delete', methods=['POST'])
@login_required
def page_delete(page_id):
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    flash('Page deleted.', 'info')
    return redirect(url_for('admin.pages'))


# -------------------------------------------------------------------------
# Media Library
# -------------------------------------------------------------------------
@admin_bp.route('/media')
@login_required
def media():
    items = Media.query.order_by(Media.created_at.desc()).all()
    return render_template('admin/media.html', media=items)


@admin_bp.route('/media/upload', methods=['POST'])
@login_required
def media_upload():
    if 'file' not in request.files:
        flash('No file selected.', 'error')
        return redirect(url_for('admin.media'))

    file = request.files['file']
    if not file or file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('admin.media'))

    if file and allowed_file(file.filename):
        raw_name = secure_filename(file.filename)
        filename = f"{int(datetime.utcnow().timestamp())}_{raw_name}"
        upload_dir = current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.static_folder, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        rel_path = f"/uploads/{filename}"
        media_item = Media(
            filename=filename,
            original_name=raw_name,
            file_path=rel_path,
            file_type=file.mimetype or 'application/octet-stream',
            file_size=os.path.getsize(file_path),
            alt_text=request.form.get('alt_text', '')
        )
        db.session.add(media_item)
        db.session.commit()
        flash('File uploaded successfully.', 'success')
    else:
        flash('Unsupported file type.', 'error')

    return redirect(url_for('admin.media'))


@admin_bp.route('/media/<int:media_id>/delete', methods=['POST'])
@login_required
def media_delete(media_id):
    item = Media.query.get_or_404(media_id)
    upload_dir = current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.static_folder, 'uploads')
    local_path = os.path.join(upload_dir, item.filename)
    if os.path.exists(local_path):
        try:
            os.remove(local_path)
        except OSError:
            pass

    db.session.delete(item)
    db.session.commit()
    flash('Media item deleted.', 'info')
    return redirect(url_for('admin.media'))


# -------------------------------------------------------------------------
# Appearance: Themes, Layout, Menus, Widgets
# -------------------------------------------------------------------------
from ..utils.theme_presets import THEME_PRESETS, apply_theme_preset

THEME_KITS = [
    {
        'key': k,
        'name': p['name'],
        'badge': p.get('badge', 'Ready Kit'),
        'category': p.get('category', ''),
        'description': p.get('description', ''),
        'color': p.get('color', '#022d62'),
        'accent': p.get('accent', '#ef3139'),
        'status': 'active'
    }
    for k, p in THEME_PRESETS.items()
]


@admin_bp.route('/appearance/themes', methods=['GET', 'POST'])
@login_required
def themes():
    if request.method == 'POST':
        theme_key = request.form.get('theme_key')
        if theme_key in THEME_PRESETS:
            success, msg = apply_theme_preset(theme_key)
            if success:
                flash(msg, 'success')
            else:
                flash(f'Failed to apply theme preset: {msg}', 'error')
        else:
            flash('Invalid theme preset selected.', 'error')
        return redirect(url_for('admin.themes'))

    active_theme = SiteSetting.get('active_theme', 'quizhub')
    return render_template('admin/themes.html', themes=THEME_KITS, active_theme=active_theme)


@admin_bp.route('/appearance/layout', methods=['GET', 'POST'])
@login_required
def layout():
    """Homepage layout and modular section manager with deep field customization."""
    active_theme = SiteSetting.get('active_theme', 'quizhub')

    if request.method == 'POST':
        SiteSetting.set('home_hero_title', request.form.get('home_hero_title', ''))
        SiteSetting.set('home_hero_subtitle', request.form.get('home_hero_subtitle', ''))
        SiteSetting.set('home_hero_button_label', request.form.get('home_hero_button_label', ''))
        SiteSetting.set('home_hero_button_url', request.form.get('home_hero_button_url', ''))
        SiteSetting.set('layout_accent_color', request.form.get('layout_accent_color', '#ef3139'))

        # Process homepage module orders and enabled states (supports IDs or legacy module_type strings)
        deleted_ids_raw = request.form.get('deleted_module_ids', '')
        deleted_ids = set([int(i.strip()) for i in deleted_ids_raw.split(',') if i.strip().isdigit()])

        module_order_raw = request.form.get('module_order', '')
        ordered_items = [i.strip() for i in module_order_raw.split(',') if i.strip()]
        enabled_items = [str(i).strip() for i in request.form.getlist('enabled_modules') if str(i).strip()]

        all_home = PageModule.query.filter(
            PageModule.is_home == True,
            (PageModule.theme == active_theme) | (PageModule.theme == None)
        ).all()
        id_map = {m.id: m for m in all_home}
        type_map = {m.module_type: m for m in all_home}

        # Delete any modules explicitly removed
        for mid in deleted_ids:
            if mid in id_map:
                db.session.delete(id_map[mid])
                all_home.remove(id_map[mid])
                del id_map[mid]

        enabled_ids = set()
        for it in enabled_items:
            if it.isdigit():
                enabled_ids.add(int(it))
            elif it in type_map:
                enabled_ids.add(type_map[it].id)
            elif it == 'contact' and 'contact_form' in type_map:
                enabled_ids.add(type_map['contact_form'].id)

        curr_order = 1
        active_types = []
        handled_ids = set()

        for it in ordered_items:
            target_mod = None
            if it.isdigit() and int(it) in id_map:
                target_mod = id_map[int(it)]
            elif it in type_map:
                target_mod = type_map[it]
            elif it == 'contact' and 'contact_form' in type_map:
                target_mod = type_map['contact_form']

            if target_mod and target_mod.id not in handled_ids:
                handled_ids.add(target_mod.id)
                target_mod.sort_order = curr_order
                target_mod.theme = active_theme
                target_mod.is_enabled = (target_mod.id in enabled_ids)
                if target_mod.is_enabled:
                    active_types.append(target_mod.module_type)
                curr_order += 1

        for m in all_home:
            if m.id not in handled_ids:
                m.sort_order = curr_order
                m.theme = active_theme
                m.is_enabled = (m.id in enabled_ids)
                if m.is_enabled:
                    active_types.append(m.module_type)
                curr_order += 1

        # Keep legacy fallback updated
        SiteSetting.set('home_modules_json', json.dumps(active_types))
        db.session.commit()
        flash('Appearance layout settings saved successfully.', 'success')
        return redirect(url_for('admin.layout'))

    home_modules = PageModule.query.filter(
        PageModule.is_home == True,
        (PageModule.theme == active_theme) | (PageModule.theme == None) | (PageModule.theme == 'hisoft')
    ).order_by(PageModule.sort_order.asc()).all()

    for m in home_modules:
        if m.theme != active_theme:
            m.theme = active_theme
    if home_modules:
        db.session.commit()
    else:
        home_order = ['hero', 'daily_quiz', 'features_strip', 'about', 'services', 'case_studies', 'posts', 'testimonials', 'trust_strip', 'contact_form']
        for idx, m_type in enumerate(home_order, 1):
            defn = MODULE_DEFINITIONS.get(m_type, {})
            m = PageModule(
                is_home=True,
                theme=active_theme,
                module_type=m_type,
                title=defn.get('name', m_type.replace('_', ' ').title()),
                placement='above',
                sort_order=idx,
                is_enabled=True
            )
            m.set_config(get_default_config(m_type))
            db.session.add(m)
        db.session.commit()
        home_modules = PageModule.query.filter_by(is_home=True, theme=active_theme).order_by(PageModule.sort_order.asc()).all()

    current_preset = THEME_PRESETS.get(active_theme, {})

    return render_template(
        'admin/layout.html',
        home_modules=home_modules,
        available_modules=MODULE_DEFINITIONS,
        active_theme=active_theme,
        active_theme_name=current_preset.get('name', active_theme.capitalize()),
        settings=SiteSetting.get_all()
    )


# -------------------------------------------------------------------------
# Dynamic Page & Layout Modules API / Handlers
# -------------------------------------------------------------------------
@admin_bp.route('/modules/add', methods=['POST'])
@login_required
def module_add():
    owner_type = request.form.get('owner_type', 'home')
    owner_id = request.form.get('owner_id')
    module_type = request.form.get('module_type', 'rich_text')
    placement = request.form.get('placement', 'above')
    return_url = request.form.get('return_url') or url_for('admin.layout')

    defn = get_module_definition(module_type)
    cfg = get_default_config(module_type)

    if owner_type == 'home':
        active_theme = SiteSetting.get('active_theme', 'quizhub')
        max_order = db.session.query(db.func.max(PageModule.sort_order)).filter_by(is_home=True, theme=active_theme).scalar() or 0
        mod = PageModule(
            is_home=True,
            theme=active_theme,
            module_type=module_type,
            title=defn.get('name', module_type.replace('_', ' ').title()),
            placement='above',
            sort_order=max_order + 1,
            is_enabled=True
        )
    elif owner_type == 'page' and owner_id:
        page = Page.query.get_or_404(int(owner_id))
        max_order = db.session.query(db.func.max(PageModule.sort_order)).filter_by(page_id=page.id, placement=placement).scalar() or 0
        mod = PageModule(
            page_id=page.id,
            module_type=module_type,
            title=defn.get('name', module_type.replace('_', ' ').title()),
            placement=placement,
            sort_order=max_order + 1,
            is_enabled=True
        )
    elif owner_type == 'post' and owner_id:
        post = Post.query.get_or_404(int(owner_id))
        max_order = db.session.query(db.func.max(PageModule.sort_order)).filter_by(post_id=post.id, placement=placement).scalar() or 0
        mod = PageModule(
            post_id=post.id,
            module_type=module_type,
            title=defn.get('name', module_type.replace('_', ' ').title()),
            placement=placement,
            sort_order=max_order + 1,
            is_enabled=True
        )
    else:
        flash('Invalid module target.', 'error')
        return redirect(return_url)

    mod.set_config(cfg)
    db.session.add(mod)
    db.session.commit()
    flash(f"Added '{mod.title}' module.", 'success')
    return redirect(return_url)


@admin_bp.route('/modules/<int:module_id>/edit', methods=['GET', 'POST'])
@login_required
def module_edit(module_id):
    mod = PageModule.query.get_or_404(module_id)
    defn = get_module_definition(mod.module_type)

    # Determine parent context and default return url
    return_url = request.args.get('return_url') or request.form.get('return_url')
    parent_label = 'Homepage'
    if mod.page:
        parent_label = f"Page: {mod.page.title}"
        if not return_url:
            return_url = url_for('admin.page_edit', page_id=mod.page.id)
    elif mod.post:
        parent_label = f"Post: {mod.post.title}"
        if not return_url:
            return_url = url_for('admin.post_edit', post_id=mod.post.id)
    else:
        if not return_url:
            return_url = url_for('admin.layout')

    if request.method == 'POST':
        mod.title = (request.form.get('title') or defn.get('name', '')).strip()
        if not mod.is_home:
            mod.placement = request.form.get('placement', mod.placement)
        mod.is_enabled = bool(request.form.get('is_enabled'))

        cfg = mod.get_config()
        for k, v in request.form.items():
            if k.startswith('cfg_'):
                cfg[k[4:]] = v.strip() if isinstance(v, str) else v
        mod.set_config(cfg)
        mod.updated_at = datetime.utcnow()
        db.session.commit()

        flash(f"Module '{mod.title}' updated successfully.", 'success')
        return redirect(return_url)

    return render_template(
        'admin/module_edit.html',
        module=mod,
        defn=defn,
        parent_label=parent_label,
        return_url=return_url
    )


@admin_bp.route('/modules/<int:module_id>/delete', methods=['POST'])
@login_required
def module_delete(module_id):
    mod = PageModule.query.get_or_404(module_id)
    return_url = request.form.get('return_url') or url_for('admin.layout')
    title = mod.title or mod.module_type
    db.session.delete(mod)
    db.session.commit()
    flash(f"Module '{title}' removed.", 'info')
    return redirect(return_url)


@admin_bp.route('/modules/restore-defaults', methods=['POST'])
@login_required
def module_restore_defaults():
    owner_type = request.form.get('owner_type', 'home')
    owner_id = request.form.get('owner_id')
    return_url = request.form.get('return_url') or url_for('admin.layout')

    if owner_type == 'home':
        active_theme = SiteSetting.get('active_theme', 'quizhub')
        PageModule.query.filter_by(is_home=True, theme=active_theme).delete()
        from ..utils.theme_presets import THEME_PRESETS
        preset = THEME_PRESETS.get(active_theme)
        if preset and preset.get('modules'):
            for m_data in preset['modules']:
                m = PageModule(
                    is_home=True,
                    theme=active_theme,
                    module_type=m_data['module_type'],
                    title=m_data['title'],
                    placement='above',
                    sort_order=m_data['sort_order'],
                    is_enabled=True
                )
                m.set_config(m_data['config'])
                db.session.add(m)
        else:
            home_order = ['hero', 'features_strip', 'about', 'services', 'case_studies', 'posts', 'testimonials', 'trust_strip', 'contact_form']
            for idx, m_type in enumerate(home_order, 1):
                defn = MODULE_DEFINITIONS.get(m_type, {})
                m = PageModule(
                    is_home=True,
                    theme=active_theme,
                    module_type=m_type,
                    title=defn.get('name', m_type.replace('_', ' ').title()),
                    placement='above',
                    sort_order=idx,
                    is_enabled=True
                )
                m.set_config(get_default_config(m_type))
                db.session.add(m)
        db.session.commit()
        preset_name = preset.get('name') if preset else active_theme.capitalize()
        flash(f'Homepage layout modules restored to {preset_name} defaults.', 'success')

    elif owner_type == 'page' and owner_id:
        page = Page.query.get_or_404(int(owner_id))
        PageModule.query.filter_by(page_id=page.id).delete()
        if page.slug == 'contact' or page.template == 'contact':
            c_hero = PageModule(page_id=page.id, module_type='hero', title='Hero Banner', placement='above', sort_order=1, is_enabled=True)
            c_hero_cfg = get_default_config('hero')
            c_hero_cfg['badge'] = 'Direct Contact'
            c_hero_cfg['headline'] = "Let's Discuss Your Architecture"
            c_hero_cfg['subtext'] = "Connect directly with our senior cloud engineers and solution architects."
            c_hero.set_config(c_hero_cfg)
            db.session.add(c_hero)

            c_cards = PageModule(page_id=page.id, module_type='contact_cards', title='Contact Info Cards (3-Column)', placement='above', sort_order=2, is_enabled=True)
            c_cards.set_config(get_default_config('contact_cards'))
            db.session.add(c_cards)

            c_form = PageModule(page_id=page.id, module_type='contact_form', title='Strategy Consultation Form', placement='below', sort_order=3, is_enabled=True)
            c_form.set_config(get_default_config('contact_form'))
            db.session.add(c_form)
        elif page.slug == 'about':
            a_hero = PageModule(page_id=page.id, module_type='hero', title='Hero Banner', placement='above', sort_order=1, is_enabled=True)
            a_hero_cfg = get_default_config('hero')
            a_hero_cfg['badge'] = 'About Our Firm'
            a_hero_cfg['headline'] = "Enterprise Cloud & Digital Solutions"
            a_hero_cfg['subtext'] = "Delivering resilient containerized systems and managed infrastructure across the globe."
            a_hero.set_config(a_hero_cfg)
            db.session.add(a_hero)

            a_strip = PageModule(page_id=page.id, module_type='features_strip', title='Features Strip', placement='below', sort_order=2, is_enabled=True)
            a_strip.set_config(get_default_config('features_strip'))
            db.session.add(a_strip)
        db.session.commit()
        flash(f"Default modules restored for page '{page.title}'.", 'success')

    return redirect(return_url)


@admin_bp.route('/appearance/menus', methods=['GET', 'POST'])
@login_required
def menus():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            title = (request.form.get('title') or '').strip()
            url = (request.form.get('url') or '').strip()
            location = request.form.get('location', 'header')
            parent_id = request.form.get('parent_id')
            parent_val = int(parent_id) if parent_id and parent_id.isdigit() else None
            open_new_tab = bool(request.form.get('open_new_tab'))

            if title and url:
                max_order = db.session.query(db.func.max(MenuItem.sort_order)).filter_by(
                    location=location,
                    parent_id=parent_val
                ).scalar() or 0
                item = MenuItem(
                    title=title,
                    url=url,
                    location=location,
                    parent_id=parent_val,
                    open_new_tab=open_new_tab,
                    sort_order=max_order + 1
                )
                db.session.add(item)
                db.session.commit()
                flash('Navigation link added successfully.', 'success')

        elif action == 'move_up':
            item_id = int(request.form.get('item_id'))
            item = MenuItem.query.get(item_id)
            if item:
                prev_item = MenuItem.query.filter(
                    MenuItem.location == item.location,
                    MenuItem.parent_id == item.parent_id,
                    MenuItem.sort_order < item.sort_order
                ).order_by(MenuItem.sort_order.desc()).first()
                if prev_item:
                    prev_item.sort_order, item.sort_order = item.sort_order, prev_item.sort_order
                    db.session.commit()
                    flash('Menu item moved up.', 'success')

        elif action == 'move_down':
            item_id = int(request.form.get('item_id'))
            item = MenuItem.query.get(item_id)
            if item:
                next_item = MenuItem.query.filter(
                    MenuItem.location == item.location,
                    MenuItem.parent_id == item.parent_id,
                    MenuItem.sort_order > item.sort_order
                ).order_by(MenuItem.sort_order.asc()).first()
                if next_item:
                    next_item.sort_order, item.sort_order = item.sort_order, next_item.sort_order
                    db.session.commit()
                    flash('Menu item moved down.', 'success')

        elif action == 'edit':
            item_id = int(request.form.get('item_id'))
            item = MenuItem.query.get(item_id)
            if item:
                title = (request.form.get('title') or '').strip()
                url = (request.form.get('url') or '').strip()
                parent_id = request.form.get('parent_id')
                parent_val = int(parent_id) if parent_id and parent_id.isdigit() and int(parent_id) != item.id else None
                open_new_tab = bool(request.form.get('open_new_tab'))

                if title and url:
                    item.title = title
                    item.url = url
                    item.parent_id = parent_val
                    item.open_new_tab = open_new_tab
                    db.session.commit()
                    flash(f"Menu item '{title}' updated successfully.", 'success')

        elif action == 'reorder':
            # Drag-and-drop batch reorder
            order_data_raw = request.form.get('order_data', '[]')
            try:
                order_list = json.loads(order_data_raw)
            except Exception:
                order_list = []

            for entry in order_list:
                iid = entry.get('id')
                if iid:
                    it = MenuItem.query.get(int(iid))
                    if it:
                        if 'sort_order' in entry:
                            it.sort_order = int(entry['sort_order'])
                        if 'parent_id' in entry:
                            p_id = entry['parent_id']
                            it.parent_id = int(p_id) if p_id and str(p_id).isdigit() and int(p_id) != it.id else None

            db.session.commit()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({'status': 'ok', 'message': 'Menu arrangement saved.'})
            flash('Menu drag-and-drop arrangement saved.', 'success')

        elif action == 'delete':
            item_id = int(request.form.get('item_id'))
            item = MenuItem.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                flash('Link removed.', 'info')

        return redirect(url_for('admin.menus'))

    header_items = MenuItem.query.filter_by(location='header', parent_id=None).order_by(MenuItem.sort_order.asc()).all()
    footer_items = MenuItem.query.filter_by(location='footer', parent_id=None).order_by(MenuItem.sort_order.asc()).all()
    solutions_items = MenuItem.query.filter_by(location='solutions', parent_id=None).order_by(MenuItem.sort_order.asc()).all()
    all_header_items = MenuItem.query.filter_by(location='header', parent_id=None).order_by(MenuItem.sort_order.asc()).all()
    pages = Page.query.filter_by(status='publish').order_by(Page.title.asc()).all()
    return render_template(
        'admin/menus.html',
        header_items=header_items,
        footer_items=footer_items,
        solutions_items=solutions_items,
        all_header_items=all_header_items,
        pages=pages
    )


@admin_bp.route('/appearance/widgets', methods=['GET', 'POST'])
@login_required
def widgets():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            sidebar_id = request.form.get('sidebar_id', 'sidebar-right')
            widget_type = request.form.get('widget_type', 'recent_posts')
            title = (request.form.get('title') or '').strip()
            content = request.form.get('content', '')
            max_order = db.session.query(db.func.max(SidebarWidget.sort_order)).filter_by(sidebar_id=sidebar_id).scalar() or 0
            w = SidebarWidget(
                sidebar_id=sidebar_id,
                widget_type=widget_type,
                title=title,
                content=content,
                sort_order=max_order + 1
            )
            cfg = {
                'font_color': request.form.get('font_color', 'default'),
                'font_color_custom': request.form.get('font_color_custom', '').strip(),
                'font_opacity': request.form.get('font_opacity', '100'),
                'font_style': request.form.get('font_style', 'sans'),
                'accent_color': request.form.get('accent_color', '#022d62'),
                'accent_color_custom': request.form.get('accent_color_custom', '').strip(),
                'accent_opacity': request.form.get('accent_opacity', '100'),
                'bg_color': request.form.get('bg_color', '#f8fafc'),
                'bg_opacity': request.form.get('bg_opacity', '100'),
                'bg_style': request.form.get('bg_style', 'slate-50'),
                'menu_location': request.form.get('menu_location', 'footer'),
                'logo_url': request.form.get('logo_url', '').strip(),
                'description': request.form.get('description', '').strip(),
                'phone': request.form.get('phone', '').strip(),
                'email': request.form.get('email', '').strip()
            }
            w.set_config(cfg)
            db.session.add(w)
            db.session.commit()
            flash('Widget added successfully.', 'success')

        elif action == 'edit':
            widget_id = int(request.form.get('widget_id'))
            w = db.session.get(SidebarWidget, widget_id)
            if not w:
                flash('Widget not found.', 'error')
                return redirect(url_for('admin.widgets'))
            w.title = (request.form.get('title') or '').strip()
            w.content = request.form.get('content', '')
            w.sidebar_id = request.form.get('sidebar_id', w.sidebar_id)
            cfg = w.get_config()
            cfg.update({
                'font_color': request.form.get('font_color', cfg.get('font_color', 'default')),
                'font_color_custom': request.form.get('font_color_custom', cfg.get('font_color_custom', '')).strip(),
                'font_opacity': request.form.get('font_opacity', cfg.get('font_opacity', '100')),
                'font_style': request.form.get('font_style', cfg.get('font_style', 'sans')),
                'accent_color': request.form.get('accent_color', cfg.get('accent_color', '#022d62')),
                'accent_color_custom': request.form.get('accent_color_custom', cfg.get('accent_color_custom', '')).strip(),
                'accent_opacity': request.form.get('accent_opacity', cfg.get('accent_opacity', '100')),
                'bg_color': request.form.get('bg_color', cfg.get('bg_color', '#f8fafc')),
                'bg_opacity': request.form.get('bg_opacity', cfg.get('bg_opacity', '100')),
                'bg_style': request.form.get('bg_style', cfg.get('bg_style', 'slate-50')),
                'menu_location': request.form.get('menu_location', cfg.get('menu_location', 'footer')),
                'logo_url': request.form.get('logo_url', cfg.get('logo_url', '')).strip(),
                'description': request.form.get('description', cfg.get('description', '')).strip(),
                'phone': request.form.get('phone', cfg.get('phone', '')).strip(),
                'email': request.form.get('email', cfg.get('email', '')).strip()
            })
            w.set_config(cfg)
            db.session.commit()
            flash('Widget updated successfully.', 'success')

        elif action in ('move_up', 'move_down'):
            widget_id = int(request.form.get('widget_id', 0))
            w = db.session.get(SidebarWidget, widget_id)
            if w:
                all_w = SidebarWidget.query.filter_by(sidebar_id=w.sidebar_id)\
                    .order_by(SidebarWidget.sort_order.asc(), SidebarWidget.id.asc()).all()
                idx = -1
                for i, item in enumerate(all_w):
                    if item.id == w.id:
                        idx = i
                        break
                if idx != -1:
                    target_idx = idx - 1 if action == 'move_up' else idx + 1
                    if 0 <= target_idx < len(all_w):
                        all_w[idx], all_w[target_idx] = all_w[target_idx], all_w[idx]
                        for seq, item in enumerate(all_w, start=1):
                            item.sort_order = seq
                        db.session.commit()
                        flash(f'Widget moved {"up" if action == "move_up" else "down"}.', 'success')

        elif action == 'delete':
            widget_id = int(request.form.get('widget_id'))
            w = db.session.get(SidebarWidget, widget_id)
            if w:
                db.session.delete(w)
                db.session.commit()
                flash('Widget removed.', 'info')

        return_url = request.form.get('return_url')
        if return_url:
            return redirect(return_url)
        return redirect(url_for('admin.widgets'))

    left_widgets = SidebarWidget.query.filter_by(sidebar_id='sidebar-left').order_by(SidebarWidget.sort_order.asc()).all()
    right_widgets = SidebarWidget.query.filter_by(sidebar_id='sidebar-right').order_by(SidebarWidget.sort_order.asc()).all()
    footer_col1_widgets = SidebarWidget.query.filter_by(sidebar_id='footer-1').order_by(SidebarWidget.sort_order.asc()).all()
    footer_col2_widgets = SidebarWidget.query.filter_by(sidebar_id='footer-2').order_by(SidebarWidget.sort_order.asc()).all()
    footer_col3_widgets = SidebarWidget.query.filter_by(sidebar_id='footer-3').order_by(SidebarWidget.sort_order.asc()).all()
    footer_col4_widgets = SidebarWidget.query.filter_by(sidebar_id='footer-4').order_by(SidebarWidget.sort_order.asc()).all()
    return render_template(
        'admin/widgets.html',
        left_widgets=left_widgets,
        right_widgets=right_widgets,
        col1_widgets=footer_col1_widgets,
        col2_widgets=footer_col2_widgets,
        col3_widgets=footer_col3_widgets,
        col4_widgets=footer_col4_widgets
    )


@admin_bp.route('/appearance/footer', methods=['GET', 'POST'])
@login_required
def footer_settings():
    """Configure multi-column footer widgets, brand logo, styling, and navigation links."""
    if request.method == 'POST':
        # Handle footer logo upload or URL
        logo_file = request.files.get('footer_logo_file')
        if logo_file and logo_file.filename and allowed_file(logo_file.filename):
            filename = secure_filename(f"footer_logo_{int(datetime.utcnow().timestamp())}_{logo_file.filename}")
            upload_dir = current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            logo_file.save(os.path.join(upload_dir, filename))
            SiteSetting.set('footer_logo', f"/static/uploads/{filename}")
        elif 'footer_logo' in request.form:
            SiteSetting.set('footer_logo', request.form.get('footer_logo', '').strip())

        SiteSetting.set('footer_style', request.form.get('footer_style', 'columns_4'))
        SiteSetting.set('footer_bg_color', request.form.get('footer_bg_color', '#022d62'))
        SiteSetting.set('footer_bg_opacity', request.form.get('footer_bg_opacity', '100'))
        SiteSetting.set('footer_text_color', request.form.get('footer_text_color', '#cbd5e1'))
        SiteSetting.set('footer_text_opacity', request.form.get('footer_text_opacity', '100'))
        SiteSetting.set('footer_accent_color', request.form.get('footer_accent_color', '#ef3139'))
        SiteSetting.set('footer_accent_opacity', request.form.get('footer_accent_opacity', '100'))
        SiteSetting.set('footer_about_text', request.form.get('footer_about_text', ''))
        SiteSetting.set('footer_copyright', request.form.get('footer_copyright', ''))
        SiteSetting.set('footer_attribution', request.form.get('footer_attribution', '').strip())

        flash('Footer styling and column settings updated successfully!', 'success')
        return redirect(url_for('admin.footer_settings'))

    settings = SiteSetting.get_all()
    col1 = SidebarWidget.query.filter_by(sidebar_id='footer-1').order_by(SidebarWidget.sort_order.asc()).all()
    col2 = SidebarWidget.query.filter_by(sidebar_id='footer-2').order_by(SidebarWidget.sort_order.asc()).all()
    col3 = SidebarWidget.query.filter_by(sidebar_id='footer-3').order_by(SidebarWidget.sort_order.asc()).all()
    col4 = SidebarWidget.query.filter_by(sidebar_id='footer-4').order_by(SidebarWidget.sort_order.asc()).all()
    header_nav = MenuItem.query.filter_by(location='header', parent_id=None).all()
    footer_nav = MenuItem.query.filter_by(location='footer', parent_id=None).all()
    solutions_nav = MenuItem.query.filter_by(location='solutions', parent_id=None).all()

    return render_template(
        'admin/footer_settings.html',
        settings=settings,
        col1_widgets=col1,
        col2_widgets=col2,
        col3_widgets=col3,
        col4_widgets=col4,
        header_nav=header_nav,
        footer_nav=footer_nav,
        solutions_nav=solutions_nav
    )


@admin_bp.route('/appearance/header', methods=['GET', 'POST'])
@login_required
def header_settings():
    """Configure 5 header layout variations, color scheme, typography, and logo."""
    if request.method == 'POST':
        # Handle logo upload or URL
        logo_file = request.files.get('logo_file')
        if logo_file and logo_file.filename and allowed_file(logo_file.filename):
            filename = secure_filename(f"logo_{int(datetime.utcnow().timestamp())}_{logo_file.filename}")
            upload_dir = current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            logo_file.save(os.path.join(upload_dir, filename))
            SiteSetting.set('site_logo', f"/static/uploads/{filename}")
        elif 'site_logo' in request.form:
            SiteSetting.set('site_logo', request.form.get('site_logo', '').strip())

        SiteSetting.set('header_style', request.form.get('header_style', 'classic_sticky'))
        SiteSetting.set('header_bg_color', request.form.get('header_bg_color', '#ffffff'))
        SiteSetting.set('header_bg_opacity', request.form.get('header_bg_opacity', '100'))
        SiteSetting.set('header_text_color', request.form.get('header_text_color', '#022d62'))
        SiteSetting.set('header_text_opacity', request.form.get('header_text_opacity', '100'))
        SiteSetting.set('header_accent_color', request.form.get('header_accent_color', '#ef3139'))
        SiteSetting.set('header_accent_opacity', request.form.get('header_accent_opacity', '100'))
        SiteSetting.set('header_font_style', request.form.get('header_font_style', 'sans'))
        SiteSetting.set('header_show_topbar', '1' if request.form.get('header_show_topbar') else '0')
        SiteSetting.set('header_cta_text', request.form.get('header_cta_text', 'Get a Quote'))
        SiteSetting.set('header_cta_url', request.form.get('header_cta_url', '/contact'))

        flash('Header layout styles and branding updated successfully!', 'success')
        return redirect(url_for('admin.header_settings'))

    settings = SiteSetting.get_all()
    return render_template('admin/header_settings.html', settings=settings)


# -------------------------------------------------------------------------
# Settings: General, Reading, SEO
# -------------------------------------------------------------------------
@admin_bp.route('/settings/general', methods=['GET', 'POST'])
@login_required
def settings_general():
    if request.method == 'POST':
        # Handle logo upload or custom URL
        logo_file = request.files.get('logo_file')
        if logo_file and logo_file.filename and allowed_file(logo_file.filename):
            filename = secure_filename(f"logo_{int(datetime.utcnow().timestamp())}_{logo_file.filename}")
            upload_dir = current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            logo_file.save(os.path.join(upload_dir, filename))
            SiteSetting.set('site_logo', f"/static/uploads/{filename}")
        elif 'site_logo' in request.form:
            SiteSetting.set('site_logo', request.form.get('site_logo', '').strip())

        SiteSetting.set('site_title', request.form.get('site_title', 'SiteBuilder Express'))
        SiteSetting.set('site_tagline', request.form.get('site_tagline', ''))
        SiteSetting.set('contact_email', request.form.get('contact_email', ''))
        SiteSetting.set('contact_phone', request.form.get('contact_phone', ''))
        SiteSetting.set('contact_address', request.form.get('contact_address', ''))
        SiteSetting.set('social_facebook', request.form.get('social_facebook', ''))
        SiteSetting.set('social_twitter', request.form.get('social_twitter', ''))
        SiteSetting.set('social_instagram', request.form.get('social_instagram', ''))
        SiteSetting.set('social_youtube', request.form.get('social_youtube', ''))
        flash('General settings updated.', 'success')
        return redirect(url_for('admin.settings_general'))

    return render_template('admin/settings_general.html', settings=SiteSetting.get_all())


@admin_bp.route('/settings/reading', methods=['GET', 'POST'])
@login_required
def settings_reading():
    pages = Page.query.filter_by(status='publish').order_by(Page.title.asc()).all()
    if request.method == 'POST':
        SiteSetting.set('homepage_type', request.form.get('homepage_type', 'posts'))
        SiteSetting.set('homepage_page_id', request.form.get('homepage_page_id', ''))
        SiteSetting.set('posts_per_page', request.form.get('posts_per_page', '10'))
        flash('Reading settings updated.', 'success')
        return redirect(url_for('admin.settings_reading'))

    return render_template('admin/settings_reading.html', settings=SiteSetting.get_all(), pages=pages)


@admin_bp.route('/settings/seo', methods=['GET', 'POST'])
@login_required
def settings_seo():
    if request.method == 'POST':
        SiteSetting.set('meta_title', request.form.get('meta_title', ''))
        SiteSetting.set('meta_description', request.form.get('meta_description', ''))
        SiteSetting.set('meta_keywords', request.form.get('meta_keywords', ''))
        SiteSetting.set('default_og_image', request.form.get('default_og_image', ''))
        SiteSetting.set('google_analytics_id', request.form.get('google_analytics_id', ''))
        SiteSetting.set('google_site_verification', request.form.get('google_site_verification', ''))
        flash('SEO & Analytics settings updated.', 'success')
        return redirect(url_for('admin.settings_seo'))

    return render_template('admin/settings_seo.html', settings=SiteSetting.get_all())


# -------------------------------------------------------------------------
# Quizmondo Arena & Game Management
# -------------------------------------------------------------------------
@admin_bp.route('/questions')
@login_required
def questions():
    category = request.args.get('category')
    status_filter = request.args.get('status')
    community_filter = request.args.get('community')
    search = request.args.get('q', '').strip()
    
    query = QuizQuestion.query
    if category:
        query = query.filter_by(category_slug=category)
    if status_filter in ('approved', 'pending', 'rejected'):
        query = query.filter_by(status=status_filter)
    if community_filter == '1':
        query = query.filter_by(is_community=True)
    elif community_filter == '0':
        query = query.filter_by(is_community=False)
    if search:
        query = query.filter(QuizQuestion.prompt.ilike(f'%{search}%'))
        
    all_questions = query.order_by(QuizQuestion.id.desc()).all()
    categories = db.session.query(QuizQuestion.category_slug, QuizQuestion.category_name).distinct().all()
    packs = QuizPack.query.all()
    pending_count = QuizQuestion.query.filter_by(status='pending').count()
    
    return render_template(
        'admin/questions.html',
        questions=all_questions,
        categories=categories,
        packs=packs,
        current_category=category,
        current_status=status_filter,
        current_community=community_filter,
        pending_count=pending_count,
        search=search
    )


@admin_bp.route('/questions/<int:id>/status', methods=['POST'])
@login_required
def question_set_status(id):
    q = QuizQuestion.query.get_or_404(id)
    new_status = request.form.get('status', 'approved')
    if new_status in ('approved', 'pending', 'rejected'):
        q.status = new_status
        db.session.commit()
        flash(f'Question #{q.id} status updated to {new_status.capitalize()}.', 'success')
    return redirect(request.referrer or url_for('admin.questions'))


@admin_bp.route('/questions/new', methods=['GET', 'POST'])
@login_required
def question_new():
    if request.method == 'POST':
        prompt = (request.form.get('prompt') or '').strip()
        cat_slug = (request.form.get('category_slug') or 'general').strip()
        cat_name = (request.form.get('category_name') or 'General').strip()
        difficulty = request.form.get('difficulty', 'medium')
        correct = request.form.get('correct_option', 'A').strip().upper()
        explanation = request.form.get('explanation', '').strip()
        
        options = {
            'A': request.form.get('opt_a', '').strip(),
            'B': request.form.get('opt_b', '').strip(),
            'C': request.form.get('opt_c', '').strip(),
            'D': request.form.get('opt_d', '').strip()
        }
        
        if not prompt or not options['A'] or not options['B']:
            flash('Prompt and at least options A and B are required.', 'error')
            return redirect(url_for('admin.question_new'))
            
        q = QuizQuestion(
            prompt=prompt,
            category_slug=cat_slug,
            category_name=cat_name,
            difficulty=difficulty,
            options_json=json.dumps(options),
            correct_option=correct,
            explanation=explanation,
            points=100,
            time_limit=15
        )
        db.session.add(q)
        db.session.commit()
        flash('Question created successfully in arena bank.', 'success')
        return redirect(url_for('admin.questions'))
        
    categories = db.session.query(QuizQuestion.category_slug, QuizQuestion.category_name).distinct().all()
    return render_template('admin/question_edit.html', question=None, categories=categories)


@admin_bp.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def question_edit(id):
    q = QuizQuestion.query.get_or_404(id)
    if request.method == 'POST':
        q.prompt = (request.form.get('prompt') or '').strip()
        q.category_slug = (request.form.get('category_slug') or 'general').strip()
        q.category_name = (request.form.get('category_name') or 'General').strip()
        q.difficulty = request.form.get('difficulty', 'medium')
        q.correct_option = request.form.get('correct_option', 'A').strip().upper()
        q.explanation = request.form.get('explanation', '').strip()
        
        options = {
            'A': request.form.get('opt_a', '').strip(),
            'B': request.form.get('opt_b', '').strip(),
            'C': request.form.get('opt_c', '').strip(),
            'D': request.form.get('opt_d', '').strip()
        }
        q.options_json = json.dumps(options)
        db.session.commit()
        flash('Question updated successfully.', 'success')
        return redirect(url_for('admin.questions'))
        
    categories = db.session.query(QuizQuestion.category_slug, QuizQuestion.category_name).distinct().all()
    return render_template('admin/question_edit.html', question=q, categories=categories, options=q.get_options())


@admin_bp.route('/questions/<int:id>/delete', methods=['POST'])
@login_required
def question_delete(id):
    q = QuizQuestion.query.get_or_404(id)
    db.session.delete(q)
    db.session.commit()
    flash('Question removed from arena.', 'success')
    return redirect(url_for('admin.questions'))


@admin_bp.route('/questions/import', methods=['POST'])
@login_required
def questions_import():
    file = request.files.get('pack_file')
    if not file or not file.filename.endswith('.json'):
        flash('Please upload a valid JSON pack file.', 'error')
        return redirect(url_for('admin.questions'))
        
    try:
        data = json.load(file)
        imported_count = 0
        pack_title = data.get('title', 'Imported Pack')
        pack_slug = data.get('slug', slugify(pack_title))
        cat_slug = data.get('category_slug', 'general')
        
        pack = QuizPack.query.filter_by(slug=pack_slug).first()
        if not pack:
            pack = QuizPack(
                title=pack_title,
                slug=pack_slug,
                description=data.get('description', ''),
                icon=data.get('icon', '📦'),
                category_slug=cat_slug,
                author_name='Admin Import'
            )
            db.session.add(pack)
            db.session.flush()
            
        for q_item in data.get('questions', []):
            prompt = q_item.get('prompt')
            if not prompt or QuizQuestion.query.filter_by(prompt=prompt).first():
                continue
            q = QuizQuestion(
                prompt=prompt,
                options_json=json.dumps(q_item.get('options', {})),
                correct_option=q_item.get('correct', 'A'),
                explanation=q_item.get('explanation', ''),
                category_slug=cat_slug,
                category_name=pack_title,
                difficulty=q_item.get('difficulty', 'medium'),
                pack_slug=pack_slug,
                points=100,
                time_limit=15
            )
            db.session.add(q)
            imported_count += 1
            
        db.session.commit()
        flash(f'Successfully imported {imported_count} questions from pack "{pack_title}".', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Import error: {str(e)}', 'error')
        
    return redirect(url_for('admin.questions'))


@admin_bp.route('/questions/export')
@login_required
def questions_export():
    all_q = QuizQuestion.query.all()
    export_data = {
        'title': 'Quizmondo Master Question Pack',
        'slug': 'quizmondo-master-export',
        'exported_at': datetime.utcnow().isoformat(),
        'questions': [
            {
                'prompt': q.prompt,
                'options': q.get_options(),
                'correct': q.correct_option,
                'explanation': q.explanation,
                'category_slug': q.category_slug,
                'category_name': q.category_name,
                'difficulty': q.difficulty
            }
            for q in all_q
        ]
    }
    from flask import Response
    return Response(
        json.dumps(export_data, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=quizmondo_questions_export.json'}
    )


def _verify_admin_password(password_attempt: str) -> bool:
    """Verify the admin's password for destructive maintenance actions (clear duels, clear content, etc.)."""
    pw = (password_attempt or '').strip()
    if not pw:
        return False
    uid = session.get('user_id')
    if uid:
        curr_u = db.session.get(User, uid)
        if curr_u and curr_u.check_password(pw):
            return True
    admin_users = User.query.filter(User.role.in_(['super_admin', 'admin'])).all()
    for au in admin_users:
        if au.check_password(pw):
            return True
    return False


@admin_bp.route('/duels')
@login_required
def duels():
    matches = ArenaMatch.query.order_by(ArenaMatch.created_at.desc()).all()
    return render_template('admin/duels.html', matches=matches)


@admin_bp.route('/duels/<int:id>/delete', methods=['POST'])
@login_required
def duel_delete(id):
    m = ArenaMatch.query.get_or_404(id)
    code = m.match_code
    ArenaRound.query.filter_by(match_id=m.id).delete()
    db.session.delete(m)
    db.session.commit()
    flash(f'Arena Duel #{code} deleted.', 'success')
    return redirect(request.referrer or url_for('admin.duels'))


@admin_bp.route('/duels/bulk-delete', methods=['POST'])
@login_required
def duels_bulk_delete():
    """Delete every duel ticked in the admin duels table in one pass."""
    ids = [int(v) for v in request.form.getlist('duel_ids') if str(v).isdigit()]
    if not ids:
        flash('No duels were selected.', 'error')
        return redirect(request.referrer or url_for('admin.duels'))

    ArenaRound.query.filter(ArenaRound.match_id.in_(ids)).delete(synchronize_session=False)
    removed = ArenaMatch.query.filter(ArenaMatch.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    flash(f'Deleted {removed} selected Arena Duel(s).', 'success')
    return redirect(request.referrer or url_for('admin.duels'))


@admin_bp.route('/system/clear', methods=['POST'])
@login_required
def system_clear():
    """Password-gated administrative maintenance to clear duels, test players, pub states, or content."""
    pw = request.form.get('admin_password') or ''
    target = (request.form.get('clear_target') or '').strip()

    if not _verify_admin_password(pw):
        flash('Action blocked: Invalid Admin Password / PIN. Please enter your valid administrator password (or set one in Profile & Password) to confirm.', 'error')
        return redirect(request.referrer or url_for('admin.dashboard'))

    if target == 'duels':
        round_cnt = ArenaRound.query.delete()
        match_cnt = ArenaMatch.query.delete()
        for p in PlayerProfile.query.all():
            p.matches_played = 0
            p.matches_won = 0
        db.session.commit()
        flash(f'Cleared all {match_cnt} Arena Duels ({round_cnt} rounds) and reset win/loss counters.', 'success')

    elif target == 'stale_duels':
        # Abandoned duels only: never past Round 1, nobody has scored a point, and
        # older than the chosen cut-off. Covers bot duels too, which are marked
        # in_progress the moment they are created and so never sit in 'waiting'.
        # A player who answered Round 1 badly still advances past Round 1, so a
        # genuinely played duel can never match this.
        try:
            days = int(request.form.get('stale_days') or 7)
        except ValueError:
            days = 7
        days = max(1, min(days, 365))
        cutoff = datetime.utcnow() - timedelta(days=days)

        candidates = ArenaMatch.query.filter(
            ArenaMatch.status.in_(['waiting', 'in_progress']),
            ArenaMatch.current_round <= 1,
            ArenaMatch.created_at < cutoff
        ).all()
        stale_ids = [
            m.id for m in candidates
            if not (m.p1_total_score or 0) and not (m.p2_total_score or 0)
        ]

        if stale_ids:
            ArenaRound.query.filter(ArenaRound.match_id.in_(stale_ids)).delete(synchronize_session=False)
            ArenaMatch.query.filter(ArenaMatch.id.in_(stale_ids)).delete(synchronize_session=False)
            db.session.commit()
        flash(
            f'Cleared {len(stale_ids)} abandoned duel(s) older than {days} day(s) '
            f'(stuck on Round 1 with no score on either side). Played and completed duels untouched.',
            'success' if stale_ids else 'info'
        )

    elif target == 'guest_players':
        guests = PlayerProfile.query.filter(PlayerProfile.user_id.is_(None)).all()
        removed = 0
        for g in guests:
            db.session.delete(g)
            removed += 1
        db.session.commit()
        flash(f'Cleared {removed} unlinked guest player sessions (all registered user accounts preserved).', 'success')

    elif target == 'community_questions':
        removed = QuizQuestion.query.filter_by(is_community=True).delete()
        db.session.commit()
        flash(f'Cleared {removed} community-submitted questions (Core packs preserved).', 'success')

    elif target == 'pub_leagues_state':
        leagues_list = PubLeague.query.all()
        for lg in leagues_list:
            st = lg.get_state()
            st['current_round'] = 1
            st['round_status'] = 'waiting'
            st['answers_revealed'] = False
            st['teams'] = []
            st['round_questions'] = {}
            st['reset_ts'] = datetime.utcnow().isoformat()
            lg.set_state(st)
        db.session.commit()
        flash(f'Reset all {len(leagues_list)} Pub Quiz Leagues to Round 1 waiting state and cleared active tables.', 'success')

    elif target == 'cms_posts':
        removed = Post.query.delete()
        db.session.commit()
        flash(f'Cleared {removed} blog posts from CMS.', 'success')

    elif target == 'everything_test_data':
        ArenaRound.query.delete()
        match_cnt = ArenaMatch.query.delete()
        guest_cnt = PlayerProfile.query.filter(PlayerProfile.user_id.is_(None)).delete()
        for p in PlayerProfile.query.all():
            p.matches_played = 0
            p.matches_won = 0
        for lg in PubLeague.query.all():
            st = lg.get_state()
            st['current_round'] = 1
            st['round_status'] = 'waiting'
            st['answers_revealed'] = False
            st['teams'] = []
            st['round_questions'] = {}
            st['reset_ts'] = datetime.utcnow().isoformat()
            lg.set_state(st)
        db.session.commit()
        flash(f'Full Arena Reset complete: Cleared {match_cnt} duels, removed {guest_cnt} guest sessions, and reset all Pub Quiz rooms.', 'success')

    else:
        flash('Please select a valid maintenance action.', 'error')

    return redirect(request.referrer or url_for('admin.dashboard'))


@admin_bp.route('/users')
@admin_bp.route('/players')
@login_required
def players():
    search = request.args.get('q', '').strip()
    role_filter = request.args.get('role', '').strip()

    # Ensure every registered User has a linked PlayerProfile so admins can manage all accounts seamlessly
    import secrets
    all_users_objs = User.query.order_by(User.id.asc()).all()
    profiles_by_uid = {p.user_id: p for p in PlayerProfile.query.filter(PlayerProfile.user_id.isnot(None)).all()}
    created_any = False
    for u in all_users_objs:
        if u.id not in profiles_by_uid:
            prof = PlayerProfile(
                user_id=u.id,
                session_key=f"usr_{u.id}_{secrets.token_hex(6)}",
                display_name=u.username,
                avatar_key='quizzy',
                level=1,
                xp=100,
                coins=250
            )
            db.session.add(prof)
            created_any = True
    if created_any:
        db.session.commit()

    query = PlayerProfile.query
    if search:
        matching_uids = [u.id for u in all_users_objs if search.lower() in (u.username or '').lower() or search.lower() in (u.email or '').lower()]
        if matching_uids:
            query = query.filter((PlayerProfile.display_name.ilike(f'%{search}%')) | (PlayerProfile.user_id.in_(matching_uids)))
        else:
            query = query.filter(PlayerProfile.display_name.ilike(f'%{search}%'))

    all_players = query.order_by(PlayerProfile.user_id.is_(None).asc(), PlayerProfile.xp.desc()).all()
    all_users = {u.id: u for u in User.query.all()}

    if role_filter:
        if role_filter == 'guest':
            all_players = [p for p in all_players if not p.user_id]
        else:
            all_players = [p for p in all_players if p.user_id and all_users.get(p.user_id) and all_users[p.user_id].role == role_filter]

    return render_template(
        'admin/players.html',
        players=all_players,
        users_by_id=all_users,
        search=search,
        role_filter=role_filter
    )


@admin_bp.route('/users/create', methods=['POST'])
@login_required
def user_create():
    """Create a new registered User (Super Admin, Admin, Quizmaster, Creator, or Player) and linked PlayerProfile."""
    import secrets
    username = (request.form.get('username') or '').strip()
    email = (request.form.get('email') or '').strip().lower()
    role = (request.form.get('role') or 'player').strip()
    password = (request.form.get('password') or '').strip()
    coins = int(request.form.get('coins') or 250)
    xp = int(request.form.get('xp') or 100)

    if role not in ('super_admin', 'admin', 'quizmaster', 'creator', 'player'):
        role = 'player'

    if not username or not password:
        flash('Username and Password / PIN are required to create a user.', 'error')
        return redirect(url_for('admin.players'))

    if not email:
        email = f"{slugify(username)}@quizmondo.local"

    if User.query.filter((User.username.ilike(username)) | (User.email.ilike(email))).first():
        flash(f'A user with username "{username}" or email "{email}" already exists.', 'error')
        return redirect(url_for('admin.players'))

    new_user = User(username=username, email=email, role=role, is_active=True)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.flush()

    prof = PlayerProfile(
        user_id=new_user.id,
        session_key=f"usr_{new_user.id}_{secrets.token_hex(6)}",
        display_name=username,
        avatar_key=request.form.get('avatar_key') or 'quizzy',
        level=1 + (xp // 500),
        xp=xp,
        coins=coins
    )
    db.session.add(prof)
    db.session.commit()
    flash(f'User "{username}" ({role.upper()}) created successfully!', 'success')
    return redirect(url_for('admin.players'))


@admin_bp.route('/players/<int:id>/update', methods=['POST'])
@login_required
def player_update(id):
    """Update a user/player's display name, username, email, role, XP, coins, or reset their password/PIN."""
    p = PlayerProfile.query.get_or_404(id)
    display_name = (request.form.get('display_name') or '').strip()
    email = (request.form.get('email') or '').strip().lower()
    role = (request.form.get('role') or 'player').strip()
    new_password = (request.form.get('new_password') or '').strip()
    xp_val = request.form.get('xp')
    coins_val = request.form.get('coins')

    if role not in ('super_admin', 'admin', 'quizmaster', 'creator', 'player'):
        role = 'player'

    if display_name:
        p.display_name = display_name
    if xp_val is not None and str(xp_val).strip().isdigit():
        p.xp = int(xp_val)
        p.level = 1 + (p.xp // 500)
    if coins_val is not None and str(coins_val).strip().isdigit():
        p.coins = int(coins_val)

    if p.user_id:
        u = db.session.get(User, p.user_id)
        if u:
            if display_name:
                conflict = User.query.filter(User.username.ilike(display_name), User.id != u.id).first()
                if not conflict:
                    u.username = display_name
            if email:
                conflict_em = User.query.filter(User.email.ilike(email), User.id != u.id).first()
                if not conflict_em:
                    u.email = email
            u.role = role
            if new_password:
                u.set_password(new_password)
    else:
        # Upgrade guest session to a registered User account if email or password or non-guest role is supplied
        if email or new_password or role in ('super_admin', 'admin', 'quizmaster', 'creator'):
            uname = p.display_name or f"Player_{p.id}"
            if User.query.filter(User.username.ilike(uname)).first():
                uname = f"{uname}_{p.id}"
            u_email = email or f"{slugify(uname)}@quizmondo.local"
            if User.query.filter(User.email.ilike(u_email)).first():
                u_email = f"{slugify(uname)}_{p.id}@quizmondo.local"
            u = User(username=uname, email=u_email, role=role, is_active=True)
            u.set_password(new_password or '123456')
            db.session.add(u)
            db.session.flush()
            p.user_id = u.id

    db.session.commit()
    flash(f'Updated account & profile for "{p.display_name}".', 'success')
    return redirect(url_for('admin.players'))


@admin_bp.route('/players/<int:id>/delete', methods=['POST'])
@login_required
def player_delete(id):
    p = PlayerProfile.query.get_or_404(id)
    if p.user_id and p.user_id == session.get('user_id'):
        flash('You cannot delete your own active administrator account.', 'error')
        return redirect(url_for('admin.players'))

    name = p.display_name
    uid = p.user_id
    db.session.delete(p)
    if uid:
        u = db.session.get(User, uid)
        if u and u.id != session.get('user_id'):
            db.session.delete(u)
    db.session.commit()
    flash(f'Deleted user/player "{name}".', 'success')
    return redirect(url_for('admin.players'))


@admin_bp.route('/players/bulk-delete', methods=['POST'])
@login_required
def players_bulk_delete():
    """Delete every account ticked in the admin players table in one pass."""
    ids = [int(v) for v in request.form.getlist('player_ids') if str(v).isdigit()]
    if not ids:
        flash('No accounts were selected.', 'error')
        return redirect(request.referrer or url_for('admin.players'))

    me = session.get('user_id')
    removed = 0
    skipped_self = False
    for p in PlayerProfile.query.filter(PlayerProfile.id.in_(ids)).all():
        if p.user_id and p.user_id == me:
            skipped_self = True
            continue
        uid = p.user_id
        db.session.delete(p)
        if uid:
            u = db.session.get(User, uid)
            if u and u.id != me:
                db.session.delete(u)
        removed += 1
    db.session.commit()

    msg = f'Deleted {removed} selected user/player account(s).'
    if skipped_self:
        msg += ' Your own active administrator account was skipped.'
    flash(msg, 'success' if removed else 'error')
    return redirect(request.referrer or url_for('admin.players'))


@admin_bp.route('/players/<int:id>/role', methods=['POST'])
@login_required
def player_set_role(id):
    p = PlayerProfile.query.get_or_404(id)
    new_role = (request.form.get('role') or 'player').strip()
    if new_role not in ('super_admin', 'admin', 'quizmaster', 'creator', 'player'):
        new_role = 'player'
    if p.user_id:
        u = db.session.get(User, p.user_id)
        if u:
            u.role = new_role
            db.session.commit()
            flash(f'Role for {p.display_name} updated to {new_role}.', 'success')
    else:
        # Automatically create a linked User account if promoting a guest session!
        uname = p.display_name or f"Player_{p.id}"
        if User.query.filter(User.username.ilike(uname)).first():
            uname = f"{uname}_{p.id}"
        u = User(username=uname, email=f"{slugify(uname)}_{p.id}@quizmondo.local", role=new_role, is_active=True)
        u.set_password('123456')
        db.session.add(u)
        db.session.flush()
        p.user_id = u.id
        db.session.commit()
        flash(f'Promoted guest "{p.display_name}" to registered {new_role} (default PIN: 123456).', 'success')
    return redirect(url_for('admin.players'))


@admin_bp.route('/players/<int:id>/toggle-ban', methods=['POST'])
@login_required
def player_toggle_ban(id):
    p = PlayerProfile.query.get_or_404(id)
    p.is_banned = not p.is_banned
    p.ban_reason = 'Violating fair play guidelines' if p.is_banned else ''
    db.session.commit()
    status = 'banned' if p.is_banned else 'unbanned'
    flash(f'Player {p.display_name} has been {status}.', 'success')
    return redirect(url_for('admin.players'))


@admin_bp.route('/leagues', methods=['GET', 'POST'])
@login_required
def leagues():
    if request.method == 'POST':
        action = (request.form.get('action') or 'create').strip()

        if action == 'toggle_virtual':
            league = db.session.get(PubLeague, int(request.form.get('league_id') or 0))
            if not league:
                flash('League not found.', 'error')
                return redirect(url_for('admin.leagues'))
            league.is_virtual = not league.is_virtual_league()
            db.session.commit()
            mode = 'Virtual (online squads)' if league.is_virtual else 'In-house (physical venue)'
            flash(f'"{league.name}" is now run as {mode}.', 'success')
            return redirect(url_for('admin.leagues'))

        name = (request.form.get('name') or '').strip()
        venue = (request.form.get('venue_name') or '').strip()
        pin = (request.form.get('pin_code') or '').strip()
        schedule = (request.form.get('schedule_day') or '').strip()
        desc = (request.form.get('description') or '').strip()
        
        if not name or not pin:
            flash('League name and PIN code are required.', 'error')
            return redirect(url_for('admin.leagues'))
            
        league = PubLeague(
            name=name,
            slug=slugify(name),
            venue_name=venue or 'Virtual Pub Arena',
            pin_code=pin,
            schedule_day=schedule or 'Every Thursday at 20:00',
            description=desc,
            is_active=True,
            is_virtual=bool(request.form.get('is_virtual'))
        )
        db.session.add(league)
        db.session.commit()
        flash(f'Pub League "{name}" created successfully with PIN {pin}.', 'success')
        return redirect(url_for('admin.leagues'))
        
    all_leagues = PubLeague.query.order_by(PubLeague.created_at.desc()).all()
    return render_template('admin/leagues.html', leagues=all_leagues)
