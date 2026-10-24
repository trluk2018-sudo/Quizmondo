import os
import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from werkzeug.utils import secure_filename
from ..models import db, User, Post, Category, Page, Media, MenuItem, SidebarWidget, SiteSetting, PageModule, slugify
from ..utils.modules import get_default_config, get_module_definition, MODULE_DEFINITIONS
from .auth import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

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

    return render_template(
        'admin/dashboard.html',
        post_count=post_count,
        page_count=page_count,
        media_count=media_count,
        recent_posts=recent_posts,
        recent_pages=recent_pages
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
        (PageModule.theme == active_theme) | (PageModule.theme == None)
    ).order_by(PageModule.sort_order.asc()).all()

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
