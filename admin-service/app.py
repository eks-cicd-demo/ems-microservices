"""Admin Service — manage users & roles. Port 5003."""
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, BigInteger, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

from auth_utils import require_admin

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    id = Column(BigInteger, primary_key=True)
    email = Column(String(255))
    full_name = Column(String(255))
    role = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return {"service": "admin", "ok": True}


@app.get("/users")
@require_admin
def list_users():
    with SessionLocal() as s:
        rows = s.query(User).order_by(User.created_at.desc()).all()
        return jsonify([
            {"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role,
             "created_at": u.created_at.isoformat() if u.created_at else None}
            for u in rows
        ])


@app.post("/users/<int:user_id>/role")
@require_admin
def set_role(user_id: int):
    body = request.get_json(force=True) or {}
    role = body.get("role")
    if role not in ("admin", "user"):
        return jsonify({"error": "role must be 'admin' or 'user'"}), 400
    with SessionLocal() as s:
        u = s.get(User, user_id)
        if not u:
            return jsonify({"error": "Not found"}), 404
        u.role = role; s.commit()
        return jsonify({"id": u.id, "email": u.email, "role": u.role})


@app.delete("/users/<int:user_id>")
@require_admin
def delete_user(user_id: int):
    with SessionLocal() as s:
        u = s.get(User, user_id)
        if not u:
            return jsonify({"error": "Not found"}), 404
        s.delete(u); s.commit()
        return "", 204


if __name__ == "__main__":
    app.run(port=5003, debug=True)
