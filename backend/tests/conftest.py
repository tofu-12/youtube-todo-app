"""Shared test fixtures for unit and integration tests."""

import itertools
import os

import pytest
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import Session, sessionmaker

from app.config import TestSettings
from app.core.database import Base
from app.crud.schemas.tag import TagInsert
from app.crud.schemas.user import UserInsert
from app.crud.schemas.video import VideoInsert
from app.crud.tag import create_tag
from app.crud.user import create_user
from app.crud.video import create_video

# Ensure ENV is set to "test" before any app module reads it.
os.environ["ENV"] = "test"

# Tables that have an updated_at trigger in production.
TABLES_WITH_UPDATED_AT = [
    "users",
    "videos",
    "video_recurrences",
    "video_weekdays",
    "todo_histories",
    "tags",
    "video_tags",
    "workout_histories",
]

_TRIGGER_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""


def _ensure_test_database_exists(database_url: str) -> None:
    """Create the test database if it does not already exist."""
    from sqlalchemy.engine import make_url

    url = make_url(database_url)
    test_db_name = url.database

    # Connect to the default 'postgres' database to check/create the test DB.
    maintenance_url = url.set(database="postgres")
    maintenance_engine = create_engine(maintenance_url, isolation_level="AUTOCOMMIT")

    with maintenance_engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
            {"dbname": test_db_name},
        )
        if not result.scalar():
            conn.execute(text(f'CREATE DATABASE "{test_db_name}"'))

    maintenance_engine.dispose()


@pytest.fixture(scope="session")
def engine():
    """Create a SQLAlchemy engine connected to the test database."""
    settings = TestSettings()
    _ensure_test_database_exists(settings.DATABASE_URL)
    eng = create_engine(settings.DATABASE_URL)
    yield eng
    eng.dispose()


@pytest.fixture(scope="session")
def tables(engine):
    """Create all tables and triggers, drop them after the session."""
    Base.metadata.create_all(engine)

    with engine.connect() as conn:
        conn.execute(text(_TRIGGER_FUNCTION_SQL))
        for tbl in TABLES_WITH_UPDATED_AT:
            conn.execute(
                text(
                    f"DROP TRIGGER IF EXISTS tr_{tbl}_updated_at ON {tbl};"
                )
            )
            conn.execute(
                text(
                    f"CREATE TRIGGER tr_{tbl}_updated_at "
                    f"BEFORE UPDATE ON {tbl} "
                    f"FOR EACH ROW "
                    f"EXECUTE FUNCTION update_updated_at_column();"
                )
            )
        conn.commit()

    yield

    Base.metadata.drop_all(engine)

    with engine.connect() as conn:
        for tbl in TABLES_WITH_UPDATED_AT:
            conn.execute(
                text(
                    f"DROP TRIGGER IF EXISTS tr_{tbl}_updated_at ON {tbl};"
                )
            )
        conn.execute(
            text("DROP FUNCTION IF EXISTS update_updated_at_column();")
        )
        conn.commit()


@pytest.fixture()
def connection(engine, tables):
    """Provide a database connection with an outer transaction."""
    conn = engine.connect()
    yield conn
    conn.close()


@pytest.fixture()
def db(connection):
    """Provide a transactional database session for tests.

    Uses a nested transaction (SAVEPOINT) so that CRUD functions can call
    commit() while the outer transaction is rolled back at the end of each
    test, ensuring full test isolation.
    """
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    transaction.rollback()


# ---------------------------------------------------------------------------
# Factory fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def user_factory(db):
    """Factory callable that creates User records via CRUD."""
    def _create(**overrides):
        data = UserInsert(**overrides)
        return create_user(db, data)
    return _create


@pytest.fixture()
def video_factory(db):
    """Factory callable that creates Video records via CRUD."""
    counter = itertools.count(1)

    def _create(user_id, **overrides):
        n = next(counter)
        defaults = {
            "user_id": user_id,
            "name": f"Test Video {n}",
            "url": f"https://www.youtube.com/watch?v=test{n}",
        }
        defaults.update(overrides)
        data = VideoInsert(**defaults)
        return create_video(db, data)

    return _create


@pytest.fixture()
def tag_factory(db):
    """Factory callable that creates Tag records via CRUD."""
    counter = itertools.count(1)

    def _create(user_id, **overrides):
        n = next(counter)
        defaults = {
            "user_id": user_id,
            "name": f"tag-{n}",
        }
        defaults.update(overrides)
        data = TagInsert(**defaults)
        return create_tag(db, data)

    return _create


@pytest.fixture()
def sample_user(user_factory):
    """A pre-created User with default settings."""
    return user_factory()


@pytest.fixture()
def sample_video(sample_user, video_factory):
    """A pre-created Video belonging to sample_user."""
    return video_factory(sample_user.id)
