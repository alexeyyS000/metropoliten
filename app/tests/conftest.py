import sys

sys.path.append("/Users/alex1/Desktop/project/metropoliten/app")


from fastapi.testclient import TestClient
from api.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, drop_database
from db.config import DatabaseSettings
import alembic.config
import alembic.command
import pytest
from db.dal.post import PostDAL
from api.dependencies import get_postdal


client = TestClient(app)


@pytest.fixture(autouse=True, scope="session")
def make_migrations():
    settings = DatabaseSettings(db_name="databasefortest")
    create_database(settings.url)
    test_session_maker = sessionmaker(bind=create_engine(settings.url), expire_on_commit=False)
    config = alembic.config.Config()
    config.set_main_option("is_test", "True")
    config.set_main_option("script_location", "migrations")
    config.set_main_option("test_db_name", settings.db_name)
    alembic.command.upgrade(config, "head")

    def override_get_postdal():
        return PostDAL(test_session_maker)

    app.dependency_overrides[get_postdal] = override_get_postdal
    yield test_session_maker
    drop_database(DatabaseSettings(db_name="databasefortest").url)


@pytest.fixture()
def cteate_yield_remove_one(make_migrations):
    test_data = {
        "name": "test_name",
        "image_url": "test_url",
        "publication_date": "2023-08-14",
        "id": 1,
        "created": "2023-08-18T20:35:02",
        "updated": None,
    }
    PostDAL(make_migrations).get_or_create(test_data, id=test_data["id"])
    yield test_data
    PostDAL(make_migrations).delete_one(id=test_data["id"])


@pytest.fixture()
def remove_one(make_migrations):
    test_data = {
        "name": "test_name",
        "image_url": "test_url",
        "publication_date": "2023-08-14",
        "id": 1,
        "created": "2023-08-18T20:35:02",
        "updated": None,
    }
    yield test_data
    PostDAL(make_migrations).delete_one(id=test_data["id"])
