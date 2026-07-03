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
