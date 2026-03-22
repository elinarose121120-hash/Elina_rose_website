"""Tests for production vs local database configuration."""

import os
from pathlib import Path

from django.test import SimpleTestCase

from elina_rose_website.database import get_databases


class DatabaseConfigTests(SimpleTestCase):
    """DATABASE_URL selects Postgres; otherwise SQLite under base_dir."""

    def test_uses_sqlite_when_database_url_unset(self):
        prior = os.environ.pop('DATABASE_URL', None)
        try:
            db = get_databases(Path('/tmp/elina_test'))
        finally:
            if prior is not None:
                os.environ['DATABASE_URL'] = prior

        self.assertEqual(db['default']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(db['default']['NAME'], Path('/tmp/elina_test') / 'db.sqlite3')

    def test_uses_postgres_when_database_url_set(self):
        url = 'postgres://user:pass@example.com:5432/dbname'
        prior = os.environ.get('DATABASE_URL')
        try:
            os.environ['DATABASE_URL'] = url
            db = get_databases(Path('/tmp/elina_test'))
        finally:
            if prior is not None:
                os.environ['DATABASE_URL'] = prior
            else:
                os.environ.pop('DATABASE_URL', None)

        self.assertEqual(db['default']['ENGINE'], 'django.db.backends.postgresql')
