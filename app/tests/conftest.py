import sys

sys.path.append("/Users/alex1/Desktop/project/metropoliten/app")


from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)

from sqlalchemy_utils import create_database, drop_database
from db.config import DatabaseSettings
import alembic.config
import alembic.command
import pytest
from db.dal.post import PostDAL
from db.client import test_sesson_marker
from api.dependencies import get_postdal, override_get_postdal


@pytest.fixture(autouse=True, scope="session")
def make_migrations():
    create_database(DatabaseSettings().test_url)
    config = alembic.config.Config()
    config.set_main_option("is_test", "True")
    config.set_main_option("script_location", "migrations")
    alembic.command.upgrade(config, "head")
    yield
    drop_database(DatabaseSettings().test_url)


test_data = {"id": 1, "name": "test_name", "image_url": "test_url", "publication_date": "2023-08-14"}

app.dependency_overrides[get_postdal] = override_get_postdal


@pytest.fixture()
def cteate_yield_remove_one():
    test_object = PostDAL(test_sesson_marker).get_or_create(test_data, id=test_data["id"])
    print(test_object[1])
    yield test_object[0]
    PostDAL(test_sesson_marker).delete_one(id=test_data["id"])


@pytest.fixture()
def remove_one():
    yield
    PostDAL(test_sesson_marker).delete_one(id=test_data["id"])
