# Production database (Render and similar hosts)

## Overview

On platforms like Render, the app container filesystem is **ephemeral**: each deploy starts from a clean image. A **SQLite file inside the project directory is not persisted**, so data appears to “reset” on every deployment.

## Solution

Use a **managed PostgreSQL** database (Render PostgreSQL or external) and connect via the `DATABASE_URL` environment variable. The app reads `DATABASE_URL` in `elina_rose_website/database.py` and switches the default database engine accordingly.

## Render setup

1. In the Render dashboard, create a **PostgreSQL** instance (or use an existing one).
2. **Recommended:** In your **Web Service** → **Environment**, add **`DATABASE_URL`** with the value from **PostgreSQL** → **Connections** → **Internal Database URL** (or link the DB to the service so Render sets `DATABASE_URL` for you).
3. **Alternative:** Set discrete variables from the same Connections screen (no secrets in git): `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`. Example host format: `dpg-d705lkbuibrs73e47qhg-a` — use the exact host shown on your database’s Connections page if the app cannot connect.
4. Redeploy. Run migrations on deploy, e.g. build or start command includes: `python manage.py migrate` (often in a `render.yaml` or shell script).

Local development continues to use SQLite when neither `DATABASE_URL` nor the discrete Postgres variables are set. See `.env.example` for a template (copy to `.env` locally and fill in values; do not commit `.env`).

## Media files

Uploaded images under `MEDIA_ROOT` also live on the ephemeral disk unless you use **persistent disk**, **object storage** (e.g. S3), or a similar service. Plan separately if uploads must survive deploys.

## Files

- `elina_rose_website/database.py` — `get_databases()` logic
- `elina_rose_website/settings.py` — `DATABASES = get_databases(BASE_DIR)`
- `website/tests/test_database_config.py` — tests for SQLite vs Postgres selection
