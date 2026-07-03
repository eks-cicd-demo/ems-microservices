# Employee Management System — Microservices

Python Flask microservices with a shared PostgreSQL (AWS RDS) database, JWT auth, and an API Gateway. HTML/CSS/Bootstrap frontend served by the gateway.

## Architecture

```
Browser (Bootstrap UI)
        │
        ▼
  API Gateway  :5000  ── routes ──►  Auth Service       :5001  (login, register, JWT)
                                     Employee Service   :5002  (CRUD + search)
                                     Admin Service      :5003  (users & roles)
                                     Dashboard Service  :5004  (aggregated stats)
                                                │
                                                ▼
                                       PostgreSQL on AWS RDS
                                       schemas: auth, employee
```

- **Gateway** is the single origin the browser talks to. It proxies `/auth/*`, `/employees/*`, `/admin/*`, `/dashboard/*` to the right service and serves the HTML pages.
- **Auth Service** issues JWTs. Every other service verifies the JWT locally with the shared `JWT_SECRET` — no cross-service DB reads for auth.
- **Admin & Dashboard** talk to the DB directly (same RDS instance, `auth` + `employee` schemas). This is the pragmatic "microservices with a shared DB" pattern; splitting DBs later is a config change.

## Prerequisites

- Python 3.10+
- An AWS RDS PostgreSQL instance you can reach from your machine (security-group inbound 5432 open to your IP).

## One-time database setup

Connect to your RDS instance with `psql` and run `schema.sql`:

```bash
psql "postgresql://<user>:<pass>@<rds-endpoint>:5432/<db>" -f schema.sql
```

This creates the `auth` and `employee` schemas, tables, and the seed admin user (`admin@example.com` / `admin123` — change it).

## Configure each service

Every service folder has a `.env.example`. Copy to `.env` and fill in:

```bash
for s in gateway auth-service employee-service admin-service dashboard-service; do
  cp $s/.env.example $s/.env
done
```

Set the **same** `JWT_SECRET` in every `.env`. Set `DATABASE_URL` to your RDS URL in auth/employee/admin/dashboard.

## Install & run (5 terminals)

Each service is independent — its own venv, its own port.

```bash
# Terminal 1 — Auth Service
cd auth-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask --app app run -p 5001

# Terminal 2 — Employee Service
cd employee-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask --app app run -p 5002

# Terminal 3 — Admin Service
cd admin-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask --app app run -p 5003

# Terminal 4 — Dashboard Service
cd dashboard-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask --app app run -p 5004

# Terminal 5 — Gateway (serves the UI)
cd gateway
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask --app app run -p 5000
```

On Windows use `venv\Scripts\activate`.

Open **http://127.0.0.1:5000** and sign in with `admin@example.com` / `admin123`.

## API surface (through the gateway)

| Method | Path                         | Service    | Auth       |
|--------|------------------------------|------------|------------|
| POST   | /auth/login                  | auth       | public     |
| POST   | /auth/register               | auth       | public     |
| GET    | /auth/me                     | auth       | JWT        |
| GET    | /employees                   | employee   | JWT        |
| POST   | /employees                   | employee   | JWT admin  |
| PUT    | /employees/<id>              | employee   | JWT admin  |
| DELETE | /employees/<id>              | employee   | JWT admin  |
| GET    | /employees/search?q=...      | employee   | JWT        |
| GET    | /admin/users                 | admin      | JWT admin  |
| POST   | /admin/users/<id>/role       | admin      | JWT admin  |
| GET    | /dashboard/stats             | dashboard  | JWT        |

## Notes

- To split into per-service databases later, replace each service's `DATABASE_URL` with its own RDS DB and drop the schema qualifier — the model files are already scoped.
- The gateway proxies with `requests`; swap for nginx in production.
