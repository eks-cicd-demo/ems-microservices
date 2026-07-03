"""Employee Service — CRUD + search. Port 5002."""
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, BigInteger, String, Numeric, Date, DateTime, func, or_
from sqlalchemy.orm import declarative_base, sessionmaker

from auth_utils import require_auth, require_admin

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {"schema": "employee"}
    id = Column(BigInteger, primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50))
    position = Column(String(100))
    department = Column(String(100))
    salary = Column(Numeric(12, 2))
    hire_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id, "full_name": self.full_name, "email": self.email,
            "phone": self.phone, "position": self.position, "department": self.department,
            "salary": float(self.salary) if self.salary is not None else None,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
        }


app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return {"service": "employee", "ok": True}


@app.get("/")
@require_auth
def list_employees():
    with SessionLocal() as s:
        rows = s.query(Employee).order_by(Employee.created_at.desc()).all()
        return jsonify([e.to_dict() for e in rows])


@app.get("/search")
@require_auth
def search():
    q = (request.args.get("q") or "").strip()
    with SessionLocal() as s:
        query = s.query(Employee)
        if q:
            like = f"%{q}%"
            query = query.filter(or_(
                Employee.full_name.ilike(like),
                Employee.email.ilike(like),
                Employee.position.ilike(like),
                Employee.department.ilike(like),
            ))
        return jsonify([e.to_dict() for e in query.order_by(Employee.full_name).all()])


def _payload():
    b = request.get_json(force=True) or {}
    return {k: (b.get(k) or None) for k in ("full_name", "email", "phone", "position", "department", "hire_date")} | \
           {"salary": b.get("salary")}


@app.post("/")
@require_admin
def create():
    data = _payload()
    if not data["full_name"] or not data["email"]:
        return jsonify({"error": "full_name and email are required"}), 400
    with SessionLocal() as s:
        if s.query(Employee).filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already exists"}), 409
        e = Employee(**data); s.add(e); s.commit(); s.refresh(e)
        return jsonify(e.to_dict()), 201


@app.put("/<int:emp_id>")
@require_admin
def update(emp_id: int):
    data = _payload()
    with SessionLocal() as s:
        e = s.get(Employee, emp_id)
        if not e:
            return jsonify({"error": "Not found"}), 404
        for k, v in data.items():
            setattr(e, k, v)
        s.commit(); s.refresh(e)
        return jsonify(e.to_dict())


@app.delete("/<int:emp_id>")
@require_admin
def delete(emp_id: int):
    with SessionLocal() as s:
        e = s.get(Employee, emp_id)
        if not e:
            return jsonify({"error": "Not found"}), 404
        s.delete(e); s.commit()
        return "", 204


if __name__ == "__main__":
    app.run(port=5002, debug=True)
