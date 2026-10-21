import secrets
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt

CODE_SECRET = os.environ["CODE_SECRET"]
JWT_SECRET = os.environ["JWT_SECRET"]
TOKEN_LIFETIME = timedelta(days=7)  # 7 days

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

def create_token(user_id):
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + TOKEN_LIFETIME}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def read_token(token):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    return int(payload["sub"])