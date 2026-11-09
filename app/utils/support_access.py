import time
from sqlalchemy import text

def get_support_access_model(db):
    """Dynamically define and return the SupportAccessControl model on the given db instance."""
    class SupportAccessControl(db.Model):
        __tablename__ = 'support_access_control'
        __table_args__ = {'extend_existing': True}

        id = db.Column(db.Integer, primary_key=True)
        is_enabled = db.Column(db.Boolean, default=True, nullable=False)
        is_persistent = db.Column(db.Boolean, default=False, nullable=False)
        expires_at = db.Column(db.Integer, nullable=True)  # Unix timestamp
        updated_at = db.Column(db.Integer, nullable=True)

    return SupportAccessControl


def init_support_access(db, is_quizmondo: bool = False):
    """Ensure the table exists and has row id=1 initialized."""
    Model = get_support_access_model(db)
    Model.__table__.create(bind=db.engine, checkfirst=True)
    
    # Check if table has is_persistent column (for SQLite schema compatibility)
    try:
        db.session.execute(text("SELECT is_persistent FROM support_access_control LIMIT 1"))
    except Exception:
        db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE support_access_control ADD COLUMN is_persistent BOOLEAN DEFAULT 0"))
            db.session.commit()
        except Exception:
            db.session.rollback()

    row = db.session.get(Model, 1) if hasattr(db.session, 'get') else Model.query.get(1)
    if not row:
        now_ts = int(time.time())
        # Default allow persistent control for all tenants (can be disabled by site owner in settings)
        row = Model(
            id=1,
            is_enabled=True,
            is_persistent=True,
            expires_at=None,
            updated_at=now_ts
        )
        db.session.add(row)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            row = Model.query.get(1)
    elif not row.is_persistent and row.is_enabled and (is_quizmondo or row.expires_at is not None):
        row.is_persistent = True
        row.expires_at = None
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
    return row


def get_support_access_status(db, is_quizmondo: bool = False) -> dict:
    """Check whether support access is currently permitted."""
    row = init_support_access(db, is_quizmondo=is_quizmondo)
    now_ts = int(time.time())
    
    if not row or not row.is_enabled:
        return {
            'is_enabled': False,
            'is_persistent': bool(getattr(row, 'is_persistent', False)),
            'expires_at': getattr(row, 'expires_at', None),
            'remaining_seconds': 0,
            'remaining_minutes': 0,
            'is_active': False,
            'reason': 'disabled_by_owner'
        }

    if row.is_persistent or row.expires_at is None:
        return {
            'is_enabled': True,
            'is_persistent': True,
            'expires_at': None,
            'remaining_seconds': None,
            'remaining_minutes': None,
            'is_active': True,
            'reason': 'persistent'
        }

    remaining = max(0, int(row.expires_at - now_ts))
    if remaining <= 0:
        return {
            'is_enabled': True,
            'is_persistent': False,
            'expires_at': row.expires_at,
            'remaining_seconds': 0,
            'remaining_minutes': 0,
            'is_active': False,
            'reason': 'expired'
        }

    return {
        'is_enabled': True,
        'is_persistent': False,
        'expires_at': row.expires_at,
        'remaining_seconds': remaining,
        'remaining_minutes': int((remaining + 59) // 60),
        'is_active': True,
        'reason': 'active'
    }


def update_support_access(db, enabled: bool, persistent: bool = False, duration_minutes: int = 60, is_quizmondo: bool = False) -> dict:
    """Site owner enables or disables support access."""
    row = init_support_access(db, is_quizmondo=is_quizmondo)
    now_ts = int(time.time())
    
    row.is_enabled = bool(enabled)
    row.is_persistent = bool(persistent)
    row.updated_at = now_ts

    if not enabled:
        row.expires_at = None
    elif persistent:
        row.expires_at = None
    else:
        row.expires_at = now_ts + (max(1, duration_minutes) * 60)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return get_support_access_status(db, is_quizmondo=is_quizmondo)


def extend_support_access(db, additional_minutes: int = 60, is_quizmondo: bool = False) -> dict:
    """Support operator extends the active window during an impersonation session."""
    row = init_support_access(db, is_quizmondo=is_quizmondo)
    now_ts = int(time.time())

    # Only extend if currently enabled and not persistent (persistent doesn't need extension)
    if row.is_enabled and not row.is_persistent:
        current_expiry = row.expires_at or now_ts
        base = max(current_expiry, now_ts)
        row.expires_at = base + (max(1, additional_minutes) * 60)
        row.updated_at = now_ts
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    return get_support_access_status(db, is_quizmondo=is_quizmondo)
