import secrets
import hashlib
import hmac
import os

CODE_SECRET = os.environ["CODE_SECRET"]

def is_ivc_email(email):
    cleaned = email.strip().lower()
    return cleaned.endswith("@ivc.edu")

def generate_code():
    n = secrets.randbelow(1000000)
    return f"{n:06d}"

def hash_code(code):
    return hmac.new(CODE_SECRET.encode(), code.encode(), hashlib.sha256).hexdigest()

def codes_match(code, stored_hash):
    return hmac.compare_digest(hash_code(code), stored_hash)