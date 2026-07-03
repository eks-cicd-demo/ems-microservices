"""JWT helpers used by every microservice. Verifies tokens locally with the
shared JWT_SECRET so services don't need to call auth-service on each request."""
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt
from flask import request, jsonify, g

JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-me")
JWT_ALGO = os.environ.get("JWT_ALGO", "HS256")
JWT_EXPIRES_MIN = int(os.environ.get("JWT_EXPIRES_MIN", "120"))


def issue_token(user_id: int, email: str, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MIN),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def _decode():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None, "Missing bearer token"
    token = auth.split(" ", 1)[1]
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO]), None
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except jwt.InvalidTokenError as e:
        return None, f"Invalid token: {e}"


def require_auth(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        claims, err = _decode()
        if err:
            return jsonify({"error": err}), 401
        g.user = claims
        return fn(*a, **kw)
    return wrapper


def require_admin(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        claims, err = _decode()
        if err:
            return jsonify({"error": err}), 401
        if claims.get("role") != "admin":
            return jsonify({"error": "Admin only"}), 403
        g.user = claims
        return fn(*a, **kw)
    return wrapper
