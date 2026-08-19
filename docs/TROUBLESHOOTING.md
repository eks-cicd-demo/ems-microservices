# Troubleshooting

---

## Issue

PostgreSQL Authentication Failed

Error

password authentication failed for user ems_user

Root Cause

Windows PostgreSQL service was already using port 5432.

Docker PostgreSQL was inaccessible.

Resolution

Changed Docker PostgreSQL mapping

5433:5432

Updated DATABASE_URL

Result

Successfully connected.

---

## Issue

404 Not Found

Cause

Accessed /

Solution

Use

/health

---

## Issue

405 Method Not Allowed

Cause

Browser sent GET request to POST endpoint.

Solution

Use Postman.

---

## Issue

JWT Missing

Cause

Authorization header missing.

Solution

Bearer Token

Authorization: Bearer <JWT>

Later improved using Postman Environment Variables.


Docker Troubleshooting Notes
Issue #1: Admin Service Container Failed to Start
Error
KeyError: 'DATABASE_URL'

File "/app/app.py", line 13

DATABASE_URL = os.environ["DATABASE_URL"]
Symptoms
Docker image built successfully.
Container started.
Gunicorn started successfully.
Worker process exited immediately.
Container stopped automatically.
Command Used
docker run --rm -p 5003:5003 --name ems-admin-test ems-admin:v1
Root Cause Analysis

The application expects the following environment variable:

DATABASE_URL = os.environ["DATABASE_URL"]

os.environ["DATABASE_URL"] means the variable is mandatory.

During Docker image creation, the .env file was not copied into the image because it is listed in .dockerignore.

Example:

.dockerignore

.env
.env.*

As a result:

The Docker image contained the application code.
The Docker image did not contain the .env file.
No environment variables were available inside the container.
Python raised:
KeyError: DATABASE_URL
How We Diagnosed It
Step 1

Read the last lines of the logs.

Reason: Worker failed to boot
Step 2

Find the actual exception.

KeyError: DATABASE_URL
Step 3

Open the source code.

DATABASE_URL = os.environ["DATABASE_URL"]

Confirmed that the application requires this variable.

Step 4

Review the Docker run command.

docker run ...

No -e or --env-file options were provided.

Therefore, the container had no DATABASE_URL.

Resolution Option 1 (Quick Testing)

Pass the variable manually.

docker run \
-p 5003:5003 \
-e DATABASE_URL="postgresql+psycopg://ems_user:ems_password@host.docker.internal:5432/ems_db" \
-e JWT_SECRET="my-secret-key" \
ems-admin:v1
Resolution Option 2 (Recommended for Local Development)

Create:

admin-service/.env

Run:

docker run \
--env-file .env \
-p 5003:5003 \
ems-admin:v1

Docker loads every variable from the file.

Resolution Option 3 (Docker Compose)
services:
  admin:
    build: ./admin-service

    env_file:
      - ./admin-service/.env
Resolution Option 4 (Production Kubernetes)

Do not use .env.

Use:

ConfigMaps
Secrets

Example:

env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: postgres-secret
      key: database-url
Why .env Was Missing

The Docker image was intentionally built without secrets.

Because:

.dockerignore

.env
.env.*

prevented the .env file from being copied into the image.

This follows security best practices.

Key Learning

Docker Image

Contains:

Application code
Libraries
Dependencies

Does not contain:

Passwords
Database credentials
Secrets
Environment-specific configuration

Container Runtime

Provides:

Environment variables
Secrets
Database URLs
API Keys
JWT Secrets
Debugging Flow (Production Mindset)

Whenever a container fails to start:

Container Failed
       │
       ▼
docker logs <container>
       │
       ▼
Read the LAST exception
       │
       ▼
Application Error?
       │
      Yes
       │
       ▼
Open the source code
       │
       ▼
Identify missing dependency
       │
       ▼
Configuration?
Environment Variable?
Database?
File?
Permission?
Network?
       │
       ▼
Fix the root cause

Never start by changing the Dockerfile. First determine whether the failure is due to:

Application code
Missing environment variables
Database connectivity
Networking
File permissions
Docker configuration


################################################## Sprint 5 CI with quality and security ################
Sprint Troubleshooting Notes

Sprint Goal: Implement automated quality checks and testing using GitHub Actions for the EMS Microservices project.

1. isort Failure
Issue

GitHub Actions failed due to import ordering.

Example:

import os
from flask import Flask
import requests
Root Cause

Imports were not grouped and sorted according to isort rules.

Resolution

Executed:

isort .

Configured pyproject.toml:

[tool.isort]
profile = "black"
line_length = 88
2. Flake8 E402 Error
Error
E402 module level import not at top of file

Example:

load_dotenv()

import requests
Root Cause

Imports existed after executable statements.

Resolution

Moved imports above load_dotenv().

Instead of:

load_dotenv()

import requests

Used:

import requests

load_dotenv()
3. Flake8 Line Length
Error
E501 line too long
Resolution

Configured Black and Flake8 with a consistent line length.

[tool.black]
line-length = 88

[tool.flake8]
max-line-length = 88
4. Bandit B201
Error
Flask debug=True
Root Cause

Production security issue.

Resolution

Instead of

app.run(debug=True)

Used

app.run(
    debug=os.getenv("FLASK_DEBUG", "False").lower() == "true"
)

Local:

FLASK_DEBUG=True

GitHub Actions:

FLASK_DEBUG=False
5. Root Bandit Configuration

Created

.bandit

Configured

[bandit]
exclude_dirs =
    .venv,
    venv,
    __pycache__,
    .pytest_cache,
    build,
    dist,
    .git
6. Bandit Configuration Parsing Error
Error
expected document start
Root Cause

Initially created .bandit in YAML format.

Resolution

Bandit expects INI format.

Correct:

[bandit]
exclude_dirs =
    .venv,
    venv
7. Python 3.14 Compatibility
Error

Bandit skipped files with

Constant object has no attribute s
Root Cause

Bandit 1.8.6 is not fully compatible with Python 3.14.

Resolution

Installed Python 3.12.

Created a new virtual environment.

GitHub Actions already uses Python 3.12.

8. pytest Import Error
Error
ModuleNotFoundError: app
Root Cause

Running

pytest

directly caused import path issues.

Resolution

Always execute

python -m pytest
9. Missing requests Package
Error
ModuleNotFoundError: requests
Root Cause

Virtual environment dependencies were incomplete.

Resolution

Installed development dependencies correctly.

pip install -r requirements-dev.txt
10. pip Installation Mistake

Mistakenly executed

pip install requirements-dev.txt

Correct command

pip install -r requirements-dev.txt
11. Admin Service DATABASE_URL Error
Error
KeyError: DATABASE_URL
Root Cause

GitHub Actions has no local .env.

Resolution

Created GitHub repository secrets.

Created .env dynamically inside GitHub Actions.

12. PostgreSQL Connection Refused
Error
connection refused localhost:5433
Root Cause

Database container wasn't running.

Resolution

Started PostgreSQL during workflow.

docker compose up -d postgres
13. Docker Compose Variable Error
Error
JWT_SECRET is required
Root Cause

Docker Compose parses the entire compose file.

Missing environment variables prevented parsing.

Resolution

Created .env before executing

docker compose up
14. Hostname Resolution Error
Error
failed to resolve host postgres
Root Cause

pytest runs on GitHub Runner, not inside Docker.

Container hostname

postgres

is unavailable.

Resolution

GitHub Actions DATABASE_URL uses

localhost:5433

instead of

postgres:5432
15. Auth Service Database Seeding
Observation

Schema only creates tables.

Admin user isn't inserted by SQL.

Solution

Auth Service executes

seed_admin()

during startup.

GitHub Actions starts

postgres

followed by

auth-service

before running tests.

16. Dashboard Tests Missing
Error
collected 0 items
Root Cause

No

tests/

directory existed.

Resolution

Created

dashboard-service/tests/test_app.py
17. Bandit B101
Error
assert used
Root Cause

Bandit scanned pytest test files.

Resolution

Ignored tests in .bandit

exclude_dirs =
    tests

(or excluded test directories as appropriate for your project).

18. GitHub Actions Test Infrastructure

Final workflow sequence:

Checkout
        ↓
Setup Python
        ↓
Install Dependencies
        ↓
Run Bandit
        ↓
Create .env
        ↓
docker compose up postgres
        ↓
Wait for PostgreSQL
        ↓
docker compose up auth-service
        ↓
Wait for Auth Service
        ↓
Run pytest
        ↓
docker compose down

#######Sprint 6 Troubleshooting Notes################
Docker Build Workflow
Issue

Incorrect YAML structure.

Example:

- name: Checkout Repository
- uses: actions/checkout@v4
Resolution

Corrected syntax:

- name: Checkout Repository
  uses: actions/checkout@v4
9. Trivy Action Version
Issue
Unable to resolve action
aquasecurity/trivy-action@0.28.0
Root Cause

Specified action version was unavailable.

Resolution

Updated to a valid maintained release:

uses: aquasecurity/trivy-action@v0.36.0
10. Multiple Workflow Executions
Observation

A single push triggered both:

Run Tests
Docker Build
Explanation

Both workflows were configured with identical push triggers on the same branch, so GitHub Actions correctly started both independently.

Decision

Accepted during development for simplicity. Pipeline orchestration will be revisited after the infrastructure work is complete.

Key Lessons Learned
Use Python 3.12 for compatibility with the current toolchain.
Keep Docker Compose for local development and integration testing.
Use docker build in CI to produce deployable artifacts.
Tag Docker images with immutable identifiers such as Git commit SHAs.
Scan container images before publishing them.
Build infrastructure separately from application code.
Separate Infrastructure as Code and CI/CD into dedicated repositories for better maintainability and clearer ownership.
