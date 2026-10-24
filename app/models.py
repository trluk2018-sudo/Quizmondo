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
    theme = db.Column(db.String(50), default='hisoft', index=True)

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
