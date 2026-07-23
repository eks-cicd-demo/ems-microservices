# ---- Base ----
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps (psycopg needs libpq; build-essential only if you compile wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Python deps ----
COPY requirements.txt .
RUN pip install -r requirements.txt

# ---- App code ----
COPY . .

# Non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Change this per service: 5000 gateway
EXPOSE 5000

# Use gunicorn in prod; flask dev server for local. Pick one.
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]


