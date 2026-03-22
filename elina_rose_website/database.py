"""Database configuration: local SQLite vs production (DATABASE_URL / Postgres)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import dj_database_url


def _postgres_from_discrete_env() -> Optional[dict]:
    """
    Build Postgres config from env vars (Render Connections tab / manual setup).
    Supports POSTGRES_* or standard PG* names.
    """
    host = os.environ.get('POSTGRES_HOST') or os.environ.get('PGHOST')
    if not host:
        return None
    user = os.environ.get('POSTGRES_USER') or os.environ.get('PGUSER')
    password = os.environ.get('POSTGRES_PASSWORD') or os.environ.get('PGPASSWORD')
    name = os.environ.get('POSTGRES_DB') or os.environ.get('PGDATABASE')
    if not all([user, password, name]):
        return None
    port = os.environ.get('POSTGRES_PORT') or os.environ.get('PGPORT') or '5432'
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {'sslmode': 'require'},
    }


def get_databases(base_dir: Path) -> dict:
    """
    Return Django DATABASES dict. Uses SQLite unless DATABASE_URL or Postgres
    env vars are set (e.g. Render PostgreSQL).
    """
    databases = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': base_dir / 'db.sqlite3',
        }
    }
    if os.environ.get('DATABASE_URL'):
        databases['default'] = dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    else:
        discrete = _postgres_from_discrete_env()
        if discrete:
            databases['default'] = discrete
    return databases
