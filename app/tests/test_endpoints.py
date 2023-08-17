from tests.conftest import client

from conftest import test_data


def test_create_one(remove_one):
    response = client.post("/post/", json=test_data)
    remove_one
    assert response.status_code == 200


def test_get_one(cteate_yield_remove_one):
    test_object = cteate_yield_remove_one
    response = client.get(f"/post/{test_object.id}")
    assert response.status_code == 200


def test_delete_one(cteate_yield_remove_one):
    test_object = cteate_yield_remove_one
    response = client.delete(f"/post/{test_object.id}")
    assert response.status_code == 204


update_data = {"name": "string", "image_url": "test", "publication_date": "2023-08-17"}


def test_patch_one(cteate_yield_remove_one):
    test_object = cteate_yield_remove_one
    response = client.patch(f"/post/{test_object.id}", json=update_data)
    assert response.status_code == 200


def test_put_one(cteate_yield_remove_one):
    test_object = cteate_yield_remove_one
    response = client.put(f"/post/{test_object.id}", json=update_data)
    assert response.status_code == 200
