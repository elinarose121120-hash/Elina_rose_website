# Production database (Render and similar hosts)

## Overview

On platforms like Render, the app container filesystem is **ephemeral**: each deploy starts from a clean image. A **SQLite file inside the project directory is not persisted**, so data appears to “reset” on every deployment.

## Solution

Use a **managed PostgreSQL** database (Render PostgreSQL or external) and connect via the `DATABASE_URL` environment variable. The app reads `DATABASE_URL` in `elina_rose_website/database.py` and switches the default database engine accordingly.

## Render setup

1. In the Render dashboard, create a **PostgreSQL** instance (or use an existing one).
2. Link it to your web service so Render injects `DATABASE_URL`, or set `DATABASE_URL` manually on the web service (Internal Database URL from the Postgres service).
3. Redeploy. Run migrations on deploy, e.g. build or start command includes: `python manage.py migrate` (often in a `render.yaml` or shell script).

Local development continues to use SQLite when `DATABASE_URL` is not set.

## Media files

Uploaded images under `MEDIA_ROOT` also live on the ephemeral disk unless you use **persistent disk**, **object storage** (e.g. S3), or a similar service. Plan separately if uploads must survive deploys.

## Files

- `elina_rose_website/database.py` — `get_databases()` logic
- `elina_rose_website/settings.py` — `DATABASES = get_databases(BASE_DIR)`
- `website/tests/test_database_config.py` — tests for SQLite vs Postgres selection
