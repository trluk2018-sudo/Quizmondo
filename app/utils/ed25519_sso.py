"""Asymmetric Ed25519 SSO Token Verification (`kangcono_verify` companion) with Trust-On-First-Use (TOFU) Key Pinning."""
import base64
import json
import os
import time
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

# In-memory single-use nonce tracking to prevent replay attacks during 60-90s TTL window
_USED_NONCES: dict[str, int] = {}

# In-memory cached parsed public key
_CACHED_PUBLIC_KEY = None


def _b64url_decode(data: str) -> bytes:
    pad = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def _purge_expired_nonces(now: int) -> None:
    """Evict expired nonces from memory to bound dictionary size."""
    expired = [nonce for nonce, exp in _USED_NONCES.items() if exp < now]
    for nonce in expired:
        _USED_NONCES.pop(nonce, None)


def parse_ed25519_public_key(key_input):
    """Parse an Ed25519 public key from PEM string, base64(PEM), base64(DER), or raw 32 bytes."""
    if not key_input:
        return None
    if isinstance(key_input, bytes):
        raw_str = key_input.decode('utf-8', errors='replace').strip()
    else:
        raw_str = str(key_input).strip()

    # 1. Raw PEM string
    if '-----BEGIN' in raw_str:
        try:
            return serialization.load_pem_public_key(raw_str.encode('utf-8'))
        except Exception:
            pass

    # 2. Base64 encoded: could be base64-wrapped PEM, DER bytes, or raw 32 bytes
    try:
        decoded = base64.b64decode(raw_str)
        if b'-----BEGIN' in decoded:
            return serialization.load_pem_public_key(decoded)
        try:
            return serialization.load_der_public_key(decoded)
        except Exception:
            pass
        if len(decoded) == 32:
            return Ed25519PublicKey.from_public_bytes(decoded)
    except Exception:
        pass

    return None


def public_key_to_pem(pub_key) -> str:
    """Convert parsed Ed25519PublicKey into standard PEM string."""
    if not pub_key:
        return ''
    pem_bytes = pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem_bytes.decode('utf-8').strip()


def public_key_to_raw_bytes(pub_key) -> bytes:
    """Extract raw 32-byte public key representation for exact comparison."""
    if not pub_key:
        return b''
    return pub_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )


# =====================================================================
# Trust-On-First-Use (TOFU) Database Key Pinning
# =====================================================================

# In-memory test pinning fallback when running outside Flask context (e.g. standalone test suite)
_TEST_PINNED_KEY = None


def get_pinned_public_key_raw():
    """Retrieve pinned public key from database (SystemConfiguration or SiteSetting)."""
    global _TEST_PINNED_KEY
    try:
        from flask import current_app
        if not current_app:
            return _TEST_PINNED_KEY
    except Exception:
        return _TEST_PINNED_KEY

    # 1. Check SystemConfiguration (core vertical apps & control plane)
    try:
        from ..models.it_settings import SystemConfiguration
        settings = SystemConfiguration.get_settings()
        if settings and getattr(settings, 'sso_pinned_public_key', None):
            return settings.sso_pinned_public_key.strip()
    except Exception:
        pass

    # 2. Check SiteSetting (SiteBuilder & Quizmondo)
    try:
        from ..models import SiteSetting
        pinned = SiteSetting.get('sso_pinned_public_key')
        if pinned:
            return pinned.strip()
    except Exception:
        pass

    return _TEST_PINNED_KEY


def set_pinned_public_key(key_pem: str) -> bool:
    """Permanently pin the public key into the database."""
    global _TEST_PINNED_KEY
    try:
        from flask import current_app
        if not current_app:
            _TEST_PINNED_KEY = key_pem
            return True
    except Exception:
        _TEST_PINNED_KEY = key_pem
        return True

    # 1. Update SystemConfiguration
    try:
        from ..models.it_settings import SystemConfiguration
        from ..models import db
        settings = SystemConfiguration.get_settings()
        if settings and hasattr(settings, 'sso_pinned_public_key'):
            settings.sso_pinned_public_key = key_pem
            db.session.commit()
            return True
    except Exception:
        pass

    # 2. Update SiteSetting
    try:
        from ..models import SiteSetting, db
        SiteSetting.set('sso_pinned_public_key', key_pem)
        db.session.commit()
        return True
    except Exception:
        pass

    _TEST_PINNED_KEY = key_pem
    return True


def reset_pinned_public_key() -> bool:
    """Clear pinned public key (used during authorized breakglass reset)."""
    global _TEST_PINNED_KEY
    _TEST_PINNED_KEY = None
    try:
        from flask import current_app
        if not current_app:
            return True
    except Exception:
        return True

    try:
        from ..models.it_settings import SystemConfiguration
        from ..models import db
        settings = SystemConfiguration.get_settings()
        if settings and hasattr(settings, 'sso_pinned_public_key'):
            settings.sso_pinned_public_key = None
            db.session.commit()
            return True
    except Exception:
        pass

    try:
        from ..models import SiteSetting, db
        SiteSetting.set('sso_pinned_public_key', '')
        db.session.commit()
        return True
    except Exception:
        pass

    return False


def reset_pinned_key_with_admin_password(username: str, password: str) -> tuple[bool, str]:
    """Breakglass reset: A verified local super-admin re-enters their password to reset the pinned key."""
    if not username or not password:
        return False, "Username and password required."
    try:
        from ..models.user import User
    except ImportError:
        try:
            from ..models import User
        except Exception:
            return False, "User model not found."

    try:
        u = User.query.filter_by(username=username).first()
        if not u or not u.check_password(password):
            return False, "Invalid admin credentials."
        if getattr(u, 'role', '') != 'super_admin':
            return False, "Super-admin privileges required."
        ok = reset_pinned_public_key()
        if ok:
            global _CACHED_PUBLIC_KEY
            _CACHED_PUBLIC_KEY = None
            return True, "Pinned Verify key successfully reset. Next login will re-pin the active key."
        return False, "Failed to clear pinned key."
    except Exception as e:
        return False, str(e)


def resolve_sso_public_key(public_key_input: str = None):
    """Resolve the Ed25519 public key using Trust-On-First-Use (TOFU) database pinning.

    Rules:
    1. Look up any candidate key from arguments, environment (Coolify), config, or files.
    2. Check the database for a pinned key:
       - If NO key is pinned yet: PIN the candidate key in the database (First Boot / Initial Pairing).
       - If a key IS already pinned: Enforce the pinned key. If the environment supplies a DIFFERENT
         key without cryptographic handover, reject the rogue key and keep the pinned key.
    """
    global _CACHED_PUBLIC_KEY

    # 1. Explicit argument bypass (e.g. testing)
    if public_key_input:
        parsed = parse_ed25519_public_key(public_key_input)
        if parsed:
            return parsed

    # 2. Resolve candidate key from environment, config, or files
    candidate_key = None
    for env_var in ('APP_SSO_PUBLIC_KEY', 'NELSON_SSO_PUBLIC_KEY'):
        val = os.environ.get(env_var)
        if val:
            parsed = parse_ed25519_public_key(val)
            if parsed:
                candidate_key = parsed
                break

    if not candidate_key:
        try:
            from flask import current_app
            if current_app:
                cfg_val = current_app.config.get('APP_SSO_PUBLIC_KEY')
                if cfg_val:
                    candidate_key = parse_ed25519_public_key(cfg_val)
        except Exception:
            pass

    if not candidate_key:
        candidates = [
            Path('/data/sso_public_key.pem'),
            Path('/data/keys/operator_ed25519_public.pem'),
            Path('instance/sso_public_key.pem'),
            Path('instance/keys/operator_ed25519_public.pem'),
            Path('/app/instance/sso_public_key.pem'),
            Path('/app/instance/keys/operator_ed25519_public.pem'),
            Path(__file__).resolve().parent.parent.parent / 'instance' / 'sso_public_key.pem',
            Path(__file__).resolve().parent.parent.parent.parent / 'kangcono_verify' / 'keys' / 'operator_ed25519_public.pem',
        ]
        for cand in candidates:
            try:
                if cand.is_file():
                    parsed = parse_ed25519_public_key(cand.read_bytes())
                    if parsed:
                        candidate_key = parsed
                        break
            except Exception:
                pass

    # 3. Check Database Pinning (TOFU)
    pinned_raw = get_pinned_public_key_raw()
    if pinned_raw:
        pinned_key = parse_ed25519_public_key(pinned_raw)
        if pinned_key:
            # If candidate was also provided, verify match
            if candidate_key:
                if public_key_to_raw_bytes(candidate_key) != public_key_to_raw_bytes(pinned_key):
                    # Tampering / Rogue Key Injection detected!
                    print("[SECURITY ALERT] Mismatched APP_SSO_PUBLIC_KEY detected. "
                          "Refusing to switch from pinned Verify key without cryptographic handover.")
            _CACHED_PUBLIC_KEY = pinned_key
            return pinned_key

    # 4. If no key is pinned yet, pin the candidate key on first pairing
    if candidate_key:
        try:
            set_pinned_public_key(public_key_to_pem(candidate_key))
        except Exception:
            pass
        _CACHED_PUBLIC_KEY = candidate_key
        return candidate_key

    return None


def verify_ed25519_sso_token(token: str, public_key_b64: str = None, expected_scope: str = None, expected_aud: list = None):
    """Verify an `ed25519.<payload_b64>.<sig_b64>` token signed by `kangcono_verify`.

    Returns:
        (payload_dict, None) on valid signature, unexpired timestamp, and unseen nonce.
        (None, reason_str) on failure ('missing_key', 'bad_format', 'bad_signature', 'expired', 'nonce_replayed', 'wrong_scope', 'wrong_audience').
    """
    if not token or not token.startswith('ed25519.'):
        return None, 'bad_format'
    parts = token.split('.')
    if len(parts) != 3:
        return None, 'bad_format'
    _, payload_b64, sig_b64 = parts

    pub_key = resolve_sso_public_key(public_key_b64)
    if not pub_key:
        return None, 'missing_key'

    try:
        sig_bytes = _b64url_decode(sig_b64)
        pub_key.verify(sig_bytes, payload_b64.encode('ascii'))
    except Exception:
        return None, 'bad_signature'

    try:
        payload = json.loads(_b64url_decode(payload_b64).decode('utf-8'))
    except Exception:
        return None, 'bad_format'

    now = int(time.time())
    exp = int(payload.get('exp') or 0)
    if now > exp + 5:
        return None, 'expired'

    nonce = payload.get('nonce')
    if nonce:
        if nonce in _USED_NONCES:
            return None, 'nonce_replayed'
        _USED_NONCES[nonce] = exp
        if len(_USED_NONCES) > 500:
            _purge_expired_nonces(now)

        # M3 Replay Protection: persist nonces in database table across Gunicorn workers and restarts
        try:
            from flask import has_app_context
            if has_app_context():
                try:
                    from ..models.audit import SsoUsedNonce
                    from ..models import db
                except (ImportError, ValueError):
                    try:
                        from ..models import SsoUsedNonce, db
                    except (ImportError, ValueError):
                        SsoUsedNonce, db = None, None

                if SsoUsedNonce and db:
                    from sqlalchemy.exc import IntegrityError
                    SsoUsedNonce.__table__.create(bind=db.engine, checkfirst=True)
                    try:
                        SsoUsedNonce.query.filter(SsoUsedNonce.expires_at < now).delete(synchronize_session=False)
                    except Exception:
                        pass
                    try:
                        existing = SsoUsedNonce.query.filter_by(nonce=str(nonce)[:64]).first()
                        if existing:
                            return None, 'nonce_replayed'
                        db.session.add(SsoUsedNonce(nonce=str(nonce)[:64], expires_at=exp or (now + 300)))
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()
                        return None, 'nonce_replayed'
                    except Exception:
                        db.session.rollback()
        except Exception:
            pass

    if expected_scope and payload.get('scope') != expected_scope:
        return None, 'wrong_scope'

    if expected_aud:
        aud = payload.get('aud')
        if aud and aud not in expected_aud:
            return None, 'wrong_audience'

    # Cryptographic Key Rotation Handover: if token requests rotation, update pinned key
    if payload.get('action') == 'rotate_sso_key' or payload.get('scope') == 'rotate_sso_key':
        new_key_str = payload.get('new_public_key')
        if new_key_str and parse_ed25519_public_key(new_key_str):
            new_parsed = parse_ed25519_public_key(new_key_str)
            set_pinned_public_key(public_key_to_pem(new_parsed))
            global _CACHED_PUBLIC_KEY
            _CACHED_PUBLIC_KEY = new_parsed

    return payload, None
