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