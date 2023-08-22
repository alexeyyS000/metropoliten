from fastapi.testclient import TestClient

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, drop_database
from db.config import DatabaseSettings
import alembic.config
import alembic.command
import pytest

from api.main import app
from db.dal.post import PostDAL
from api.dependencies import get_postdal
from contextlib import contextmanager


@pytest.fixture(scope="function")
def post_repo(create_session_maker):
    return PostDAL(create_session_maker)


@pytest.fixture(scope="function")
def client(post_repo):
    app.dependency_overrides[get_postdal] = lambda: post_repo  # почему именно лямбда

    with TestClient(app=app, base_url="http://test/") as test_client:
        yield test_client


def make_migrations(settings):
    config = alembic.config.Config()
    config.set_main_option("is_test", "True")
    config.set_main_option("script_location", "migrations")
    config.set_main_option("test_db_name", settings.db_name)
    alembic.command.upgrade(config, "head")


@pytest.fixture(scope="session")
def make_engine():
    settings = DatabaseSettings(db_name="databasefortest")
    create_database(settings.url)
    engine = create_engine(settings.url)
    make_migrations(settings)
    yield engine
    drop_database(settings.url)


@pytest.fixture(scope="function")
def create_session(make_engine):
    connection = make_engine.connect()  # не забыть разобраться
    transaction = connection.begin()
    session_maker = sessionmaker(bind=connection, expire_on_commit=False)
    session = session_maker()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def create_session_maker(create_session):
    def session_maker():
        yield create_session

    return contextmanager(session_maker)
