"""Asymmetric Ed25519 SSO Token Verification (`kangcono_verify` companion)."""
import base64
import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from sqlalchemy.exc import IntegrityError

# Fallback in-memory single-use nonce tracking when invoked outside a Flask DB context
_USED_NONCES: dict[str, int] = {}

# In-memory cached parsed public key (lives strictly in memory after first resolution)
_CACHED_PUBLIC_KEY = None

MAX_SSO_TOKEN_TTL_SECONDS = 60


def _b64url_decode(data: str) -> bytes:
    pad = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def _purge_expired_nonces(now: int) -> None:
    """Evict expired nonces from memory to bound dictionary size."""
    expired = [nonce for nonce, exp in _USED_NONCES.items() if exp < now]
    for nonce in expired:
        _USED_NONCES.pop(nonce, None)


def _normalize_aud(value: str) -> str:
    raw = (value or '').strip()
    if not raw:
        return ''
    if '://' in raw:
        netloc = (urlparse(raw).netloc or '').strip().lower()
        if netloc:
            return netloc
    return raw.split('/')[0].strip().lower()


def _resolve_expected_audiences(expected_aud=None) -> set[str]:
    """Determine the set of valid audience identifiers (`aud`) for this site."""
    audiences = set()
    if expected_aud:
        if isinstance(expected_aud, (list, tuple, set)):
            for item in expected_aud:
                norm = _normalize_aud(str(item))
                if norm:
                    audiences.add(norm)
                    if ':' in norm:
                        audiences.add(norm.split(':', 1)[0])
        else:
            norm = _normalize_aud(str(expected_aud))
            if norm:
                audiences.add(norm)
                if ':' in norm:
                    audiences.add(norm.split(':', 1)[0])

    try:
        from flask import has_request_context, request, current_app
        if has_request_context():
            req_host = _normalize_aud(request.host)
            if req_host:
                audiences.add(req_host)
                if ':' in req_host:
                    audiences.add(req_host.split(':', 1)[0])
                if '.' in req_host:
                    audiences.add(req_host.split('.', 1)[0])
        if current_app:
            if current_app.config.get('PLATFORM_MODE'):
                audiences.add('_control')
            pub_url = current_app.config.get('PUBLIC_URL') or os.environ.get('PUBLIC_URL') or ''
            if pub_url:
                pub_host = _normalize_aud(pub_url)
                if pub_host:
                    audiences.add(pub_host)
                    if '.' in pub_host:
                        audiences.add(pub_host.split('.', 1)[0])
    except Exception:
        pass

    sub_env = (os.environ.get('APP_SUBDOMAIN') or os.environ.get('SUBDOMAIN') or '').strip().lower()
    if sub_env:
        audiences.add(sub_env)

    return audiences


def _consume_nonce_in_db(nonce: str, exp: int, now: int) -> bool:
    """Record a single-use nonce in the site's own database (`sso_used_nonce` table)
    so every worker process refuses a replay. Falls back to in-memory tracking only
    when no Flask application context is active (e.g. standalone unit tests).
    Returns True if the nonce is fresh and recorded; False if replayed.
    """
    if not nonce:
        return False

    try:
        from flask import current_app
        if current_app:
            try:
                from ..models.audit import SsoUsedNonce
                from .. import db
            except ImportError:
                from ..models import SsoUsedNonce, db

            # Ensure table exists in case this DB was initialized prior to SsoUsedNonce
            SsoUsedNonce.__table__.create(bind=db.engine, checkfirst=True)

            try:
                SsoUsedNonce.query.filter(SsoUsedNonce.expires_at < now).delete(synchronize_session=False)
                db.session.add(SsoUsedNonce(nonce=str(nonce)[:64], expires_at=int(exp)))
                db.session.commit()
                return True
            except IntegrityError:
                db.session.rollback()
                return False
            except Exception:
                db.session.rollback()
                if SsoUsedNonce.query.filter_by(nonce=str(nonce)[:64]).first() is not None:
                    return False
                raise
    except RuntimeError:
        # Outside Flask app context
        pass

    if nonce in _USED_NONCES:
        return False
    _USED_NONCES[nonce] = exp
    if len(_USED_NONCES) > 500:
        _purge_expired_nonces(now)
    return True


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


def resolve_sso_public_key(public_key_input: str = None):
    """Resolve the Ed25519 public key from memory cache, arguments, environment, config, or persistent key files."""
    global _CACHED_PUBLIC_KEY
    if not public_key_input and _CACHED_PUBLIC_KEY is not None:
        return _CACHED_PUBLIC_KEY

    # 1. Explicit argument
    if public_key_input:
        parsed = parse_ed25519_public_key(public_key_input)
        if parsed:
            return parsed

    # 2. Environment variables
    for env_var in ('APP_SSO_PUBLIC_KEY', 'NELSON_SSO_PUBLIC_KEY'):
        val = os.environ.get(env_var)
        if val:
            parsed = parse_ed25519_public_key(val)
            if parsed:
                _CACHED_PUBLIC_KEY = parsed
                return parsed

    # 3. Flask current_app config (if running inside request/app context)
    try:
        from flask import current_app
        if current_app:
            cfg_val = current_app.config.get('APP_SSO_PUBLIC_KEY')
            if cfg_val:
                parsed = parse_ed25519_public_key(cfg_val)
                if parsed:
                    _CACHED_PUBLIC_KEY = parsed
                    return parsed
    except Exception:
        pass

    # 4. Standard filesystem candidate locations
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
                    _CACHED_PUBLIC_KEY = parsed
                    return parsed
        except Exception:
            pass

    return None


def verify_ed25519_sso_token(token: str, public_key_b64: str = None,
                             expected_scope: str = None, expected_aud=None):
    """Verify an `ed25519.<payload_b64>.<sig_b64>` token signed by `kangcono_verify`.

    Enforces:
      - Valid Ed25519 signature
      - Max 60s token lifetime (`0 < exp - iat <= 60` and `now <= exp`)
      - Scope match (`expected_scope`)
      - Audience match (`aud` must match this site)
      - Single-use nonce stored in `sso_used_nonce` DB table so every worker refuses replays.

    Returns:
        (payload_dict, None) on success.
        (None, reason_str) on failure ('missing_key', 'bad_format', 'bad_signature',
        'expired', 'wrong_scope', 'wrong_audience', 'nonce_replayed').
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
    try:
        iat = int(payload.get('iat') or 0)
        exp = int(payload.get('exp') or 0)
    except (TypeError, ValueError):
        return None, 'bad_format'

    lifetime = exp - iat
    if lifetime <= 0 or lifetime > MAX_SSO_TOKEN_TTL_SECONDS:
        return None, 'expired'
    if now > exp or iat > now + 5:
        return None, 'expired'

    if expected_scope and payload.get('scope') != expected_scope:
        return None, 'wrong_scope'

    token_aud = _normalize_aud(payload.get('aud') or '')
    token_sub = (payload.get('sub') or '').strip().lower()
    allowed_audiences = _resolve_expected_audiences(expected_aud)
    if not token_aud:
        return None, 'wrong_audience'
    if allowed_audiences:
        aud_base = token_aud.split(':', 1)[0]
        if (token_aud not in allowed_audiences
                and aud_base not in allowed_audiences
                and (not token_sub or token_sub not in allowed_audiences)):
            return None, 'wrong_audience'

    nonce = payload.get('nonce')
    if not nonce or not _consume_nonce_in_db(str(nonce), exp, now):
        return None, 'nonce_replayed'

    return payload, None
