"""RFC 6238 Time-Based One-Time Password (TOTP) and Emergency Recovery Codes.

Pure Python standard-library implementation compatible with Google Authenticator,
Microsoft Authenticator, Apple Passwords, 1Password, and Authy.
Requires zero external pip dependencies.
"""
import hmac
import hashlib
import time
import struct
import base64
import secrets
import json
import urllib.parse


def generate_totp_secret() -> str:
    """Generate a random 160-bit (20 byte) base32 secret key."""
    # 20 bytes = 160 bits (RFC 4226 recommendation)
    return base64.b32encode(secrets.token_bytes(20)).decode('ascii').rstrip('=')


def format_secret_for_display(secret_b32: str) -> str:
    """Format base32 secret in 4-character chunks for human readability."""
    s = secret_b32.strip().replace(' ', '').upper()
    return ' '.join(s[i:i+4] for i in range(0, len(s), 4))


def compute_totp(secret_b32: str, counter: int = None, interval: int = 30, digits: int = 6) -> str:
    """Compute 6-digit TOTP code for the specified counter (or current time)."""
    if counter is None:
        counter = int(time.time()) // interval

    s = secret_b32.strip().replace(' ', '').upper()
    missing_padding = len(s) % 8
    if missing_padding:
        s += '=' * (8 - missing_padding)

    key = base64.b32decode(s, casefold=True)
    msg = struct.pack('>Q', counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack('>I', digest[offset:offset+4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code).zfill(digits)


def verify_totp(secret_b32: str, code: str, interval: int = 30, digits: int = 6, window: int = 1) -> bool:
    """Verify code against secret with +/- window tolerance for clock drift (default 90s total window)."""
    if not secret_b32 or not code:
        return False
    code_str = str(code).strip().replace(' ', '').replace('-', '')
    if len(code_str) != digits or not code_str.isdigit():
        return False

    current_counter = int(time.time()) // interval
    for offset in range(-window, window + 1):
        expected = compute_totp(secret_b32, counter=current_counter + offset, interval=interval, digits=digits)
        if hmac.compare_digest(expected, code_str):
            return True
    return False


def get_totp_uri(secret_b32: str, username: str, issuer: str = "Kangcono") -> str:
    """Generate otpauth:// URI for scanning with authenticator apps."""
    clean_secret = secret_b32.strip().replace(' ', '').upper()
    clean_issuer = issuer.replace(':', '').strip()
    clean_user = username.replace(':', '').strip()
    label = f"{clean_issuer}:{clean_user}"
    params = {
        'secret': clean_secret,
        'issuer': clean_issuer,
        'algorithm': 'SHA1',
        'digits': 6,
        'period': 30
    }
    return f"otpauth://totp/{urllib.parse.quote(label)}?{urllib.parse.urlencode(params)}"


def generate_recovery_codes(count: int = 8) -> tuple[list[str], list[str]]:
    """Generate single-use backup recovery codes.
    Returns (plain_codes, hashed_codes).
    """
    plain = []
    hashed = []
    for _ in range(count):
        raw = secrets.token_hex(4).upper()
        code = f"{raw[:4]}-{raw[4:]}"
        plain.append(code)
        hashed.append(hashlib.sha256(code.encode('utf-8')).hexdigest())
    return plain, hashed


def verify_and_consume_recovery_code(entered_code: str, hashed_codes_json: str) -> tuple[bool, str]:
    """Verify single-use recovery code against stored hashes, and consume it if valid."""
    if not entered_code or not hashed_codes_json:
        return False, hashed_codes_json
    try:
        hashes = json.loads(hashed_codes_json)
        if not isinstance(hashes, list):
            return False, hashed_codes_json
    except Exception:
        return False, hashed_codes_json

    clean_code = entered_code.strip().replace(' ', '').upper()
    code_hash = hashlib.sha256(clean_code.encode('utf-8')).hexdigest()
    if code_hash in hashes:
        hashes.remove(code_hash)
        return True, json.dumps(hashes)

    return False, hashed_codes_json
