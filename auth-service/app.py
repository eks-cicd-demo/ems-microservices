"""Auth Service — login, register, /me. Port 5001."""
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, BigInteger, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

from auth_utils import issue_token, require_auth
from flask import g

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    id = Column(BigInteger, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(20), nullable=False, default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def seed_admin():
    with SessionLocal() as s:
        if not s.query(User).filter_by(email="admin@example.com").first():
            s.add(User(
                email="admin@example.com",
                password_hash=generate_password_hash("admin123"),
                full_name="Administrator",
                role="admin",
            ))
            s.commit()
            print("[auth] seeded admin@example.com / admin123")


app = Flask(__name__)
CORS(app)

with app.app_context():
    seed_admin()


@app.get("/health")
def health():
    return {"service": "auth", "ok": True}


@app.post("/login")
def login():
    body = request.get_json(force=True) or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    with SessionLocal() as s:
        user = s.query(User).filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid email or password"}), 401
        token = issue_token(user.id, user.email, user.role)
        return jsonify({
            "token": token,
            "user": {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role},
        })


@app.post("/register")
def register():
    body = request.get_json(force=True) or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    full_name = body.get("full_name") or ""
    if not email or len(password) < 6:
        return jsonify({"error": "Email and password (min 6 chars) required"}), 400
    with SessionLocal() as s:
        if s.query(User).filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409
        u = User(email=email, password_hash=generate_password_hash(password),
                 full_name=full_name, role="user")
        s.add(u); s.commit(); s.refresh(u)
        token = issue_token(u.id, u.email, u.role)
        return jsonify({"token": token, "user": {"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role}}), 201


@app.get("/me")
@require_auth
def me():
    return jsonify({"user": g.user})


if __name__ == "__main__":
    app.run(port=5001, debug=True)
