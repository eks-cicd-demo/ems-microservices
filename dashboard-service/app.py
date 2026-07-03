"""Dashboard Service — aggregated stats. Port 5004."""
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text

from auth_utils import require_auth

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return {"service": "dashboard", "ok": True}


@app.get("/stats")
@require_auth
def stats():
    with engine.connect() as c:
        total_employees = c.execute(text("SELECT COUNT(*) FROM employee.employees")).scalar_one()
        total_users     = c.execute(text("SELECT COUNT(*) FROM auth.users")).scalar_one()
        avg_salary      = c.execute(text("SELECT COALESCE(AVG(salary),0) FROM employee.employees")).scalar_one()
        by_dept = c.execute(text("""
            SELECT COALESCE(department,'(none)') AS department, COUNT(*) AS count
            FROM employee.employees GROUP BY department ORDER BY count DESC
        """)).mappings().all()
        departments = len({r["department"] for r in by_dept if r["department"] != "(none)"})
    return jsonify({
        "total_employees": total_employees,
        "total_users": total_users,
        "departments": departments,
        "avg_salary": float(avg_salary or 0),
        "by_department": [dict(r) | {"count": int(r["count"])} for r in by_dept],
    })


if __name__ == "__main__":
    app.run(port=5004, debug=True)
