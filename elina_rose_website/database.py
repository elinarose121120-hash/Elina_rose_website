"""Database configuration: local SQLite vs production (DATABASE_URL / Postgres)."""

import os
from pathlib import Path

import dj_database_url


def get_databases(base_dir: Path) -> dict:
    """
    Return Django DATABASES dict. Uses SQLite unless DATABASE_URL is set
    (e.g. Render PostgreSQL).
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
    return databases
