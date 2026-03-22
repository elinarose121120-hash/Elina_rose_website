"""Tests for production vs local database configuration."""

import os
from pathlib import Path

from django.test import SimpleTestCase

from elina_rose_website.database import get_databases


def _clear_postgres_env():
    keys = (
        'DATABASE_URL',
        'POSTGRES_HOST',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'POSTGRES_DB',
        'POSTGRES_PORT',
        'PGHOST',
        'PGUSER',
        'PGPASSWORD',
        'PGDATABASE',
        'PGPORT',
    )
    saved = {}
    for k in keys:
        if k in os.environ:
            saved[k] = os.environ.pop(k)
    return saved


def _restore_env(saved):
    for k, v in saved.items():
        os.environ[k] = v


class DatabaseConfigTests(SimpleTestCase):
    """DATABASE_URL or POSTGRES_* selects Postgres; otherwise SQLite under base_dir."""

    def test_uses_sqlite_when_no_postgres_env(self):
        saved = _clear_postgres_env()
        try:
            db = get_databases(Path('/tmp/elina_test'))
        finally:
            _restore_env(saved)

        self.assertEqual(db['default']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(db['default']['NAME'], Path('/tmp/elina_test') / 'db.sqlite3')

    def test_uses_postgres_when_database_url_set(self):
        url = 'postgres://user:pass@example.com:5432/dbname'
        saved = _clear_postgres_env()
        try:
            os.environ['DATABASE_URL'] = url
            db = get_databases(Path('/tmp/elina_test'))
        finally:
            _restore_env(saved)

        self.assertEqual(db['default']['ENGINE'], 'django.db.backends.postgresql')

    def test_database_url_takes_priority_over_discrete_postgres_vars(self):
        saved = _clear_postgres_env()
        try:
            os.environ['DATABASE_URL'] = 'postgres://a:b@host1:5432/db1'
            os.environ['POSTGRES_HOST'] = 'host2'
            os.environ['POSTGRES_USER'] = 'u'
            os.environ['POSTGRES_PASSWORD'] = 'p'
            os.environ['POSTGRES_DB'] = 'd'
            db = get_databases(Path('/tmp/elina_test'))
        finally:
            _restore_env(saved)

        self.assertEqual(db['default']['HOST'], 'host1')

    def test_uses_postgres_from_discrete_env_when_no_database_url(self):
        saved = _clear_postgres_env()
        try:
            os.environ['POSTGRES_HOST'] = 'dpg-example-host-a'
            os.environ['POSTGRES_USER'] = 'user'
            os.environ['POSTGRES_PASSWORD'] = 'secret'
            os.environ['POSTGRES_DB'] = 'mydb'
            os.environ['POSTGRES_PORT'] = '5432'
            db = get_databases(Path('/tmp/elina_test'))
        finally:
            _restore_env(saved)

        self.assertEqual(db['default']['ENGINE'], 'django.db.backends.postgresql')
        self.assertEqual(db['default']['HOST'], 'dpg-example-host-a')
        self.assertEqual(db['default']['NAME'], 'mydb')
        self.assertEqual(db['default']['OPTIONS'], {'sslmode': 'require'})
