"""API Gateway — proxies /auth, /employees, /admin, /dashboard to services,
and serves the Bootstrap UI. Port 5000."""
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, Response, render_template
from flask_cors import CORS
import requests

SERVICES = {
    "auth":       os.environ.get("AUTH_SERVICE_URL",       "http://127.0.0.1:5001"),
    "employees":  os.environ.get("EMPLOYEE_SERVICE_URL",   "http://127.0.0.1:5002"),
    "admin":      os.environ.get("ADMIN_SERVICE_URL",      "http://127.0.0.1:5003"),
    "dashboard":  os.environ.get("DASHBOARD_SERVICE_URL",  "http://127.0.0.1:5004"),
}
HOP_BY_HOP = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
              "te", "trailers", "transfer-encoding", "upgrade", "content-encoding",
              "content-length", "host"}

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)


def _proxy(service_key: str, subpath: str):
    base = SERVICES[service_key]
    url = f"{base}/{subpath}"
    headers = {k: v for k, v in request.headers.items() if k.lower() not in HOP_BY_HOP}
    try:
        r = requests.request(
            method=request.method, url=url, headers=headers,
            params=request.args, data=request.get_data(),
            cookies=request.cookies, allow_redirects=False, timeout=30,
        )
    except requests.RequestException as e:
        return Response(f'{{"error":"upstream {service_key} unreachable: {e}"}}',
                        status=502, mimetype="application/json")
    resp_headers = [(k, v) for k, v in r.headers.items() if k.lower() not in HOP_BY_HOP]
    return Response(r.content, status=r.status_code, headers=resp_headers)


@app.route("/auth/",              methods=["GET", "POST", "PUT", "DELETE"], defaults={"subpath": ""})
@app.route("/auth/<path:subpath>",methods=["GET", "POST", "PUT", "DELETE"])
def proxy_auth(subpath):      return _proxy("auth", subpath)


@app.route("/employees",                methods=["GET", "POST"])
@app.route("/employees/",               methods=["GET", "POST"], defaults={"subpath": ""})
@app.route("/employees/<path:subpath>", methods=["GET", "PUT", "DELETE"])
def proxy_employees(subpath=""): return _proxy("employees", subpath)


@app.route("/admin/",              methods=["GET", "POST", "PUT", "DELETE"], defaults={"subpath": ""})
@app.route("/admin/<path:subpath>",methods=["GET", "POST", "PUT", "DELETE"])
def proxy_admin(subpath):     return _proxy("admin", subpath)


@app.route("/dashboard/",              methods=["GET"], defaults={"subpath": ""})
@app.route("/dashboard/<path:subpath>",methods=["GET"])
def proxy_dashboard(subpath): return _proxy("dashboard", subpath)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return {"service": "gateway", "ok": True, "services": SERVICES}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
