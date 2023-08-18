from tests.conftest import client
from db.dal.post import PostDAL


def test_create_one(remove_one):
    test_object = remove_one
    response = client.post("/post/", json=test_object)
    assert response.json()["name"] == test_object["name"]
    assert response.json()["id"] == test_object["id"]
    assert response.status_code == 200


def test_get_one(cteate_yield_remove_one):
    test_object = cteate_yield_remove_one
    response = client.get(f"/post/{test_object['id']}")
    assert response.json() == test_object
    assert response.status_code == 200


def test_delete_one(cteate_yield_remove_one, make_migrations):
    test_object = cteate_yield_remove_one
    response = client.delete(f"/post/{test_object['id']}")
    session_maker = make_migrations
    assert PostDAL(session_maker).get_one_or_none(id=test_object["id"]) == None
    assert response.status_code == 204


update_data = {"name": "string", "publication_date": "2023-08-17"}


def test_patch_one(cteate_yield_remove_one):
    test_object = cteate_yield_remove_one
    response = client.patch(f"/post/{test_object['id']}", json=update_data)
    assert response.json()["id"] == test_object["id"]
    assert response.json()["name"] == update_data["name"]
    assert response.status_code == 200


def test_put_one(cteate_yield_remove_one):
    test_object = cteate_yield_remove_one
    response = client.put(f"/post/{test_object['id']}", json=update_data)
    assert response.json()["id"] == test_object["id"]
    assert response.json()["name"] == update_data["name"]
    assert response.status_code == 200
