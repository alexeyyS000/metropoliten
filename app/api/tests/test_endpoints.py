import pytest
from http import HTTPStatus
from math import ceil
from operator import itemgetter


@pytest.fixture(scope="function")
def one_post():
    test_data = {
        "name": "test_name",
        "image_url": "test_url",
        "publication_date": "2023-08-14",
    }
    return test_data


@pytest.fixture(scope="function")
def create_one_post(post_repo, one_post):
    return post_repo.create_one(**one_post)


@pytest.fixture(scope="function")
def create_five_post(post_repo, one_post):
    list_names_in_test_data = ["a", "b", "c", "d", "f"]  # faker
    list_url_in_test_data = ["f", "d", "c", "b", "a"]
    test_data_of_five_posts = []
    for i in range(0, len(list_names_in_test_data)):
        next_post = one_post
        next_post["name"] = list_names_in_test_data[i]
        next_post["image_url"] = list_url_in_test_data[i]
        post_repo.create_one(**next_post)
        test_data_of_five_posts.append(
            {
                "name": next_post["name"],
                "image_url": next_post["image_url"],
                "publication_date": next_post["publication_date"],
            }
        )
    return test_data_of_five_posts


def test_create_one(post_repo, one_post, client):
    assert not post_repo.all()
    response = client.post("/post/", json=one_post)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    for key, val in one_post.items():
        assert data[key] == val
    assert post_repo.get_one_or_none(id=data["id"])


def test_get_one(create_one_post, client, one_post):
    response = client.get(f"/post/{create_one_post.id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    for key, val in one_post.items():
        assert data[key] == val


def test_get_one_not_exist(client):
    response = client.get("/post/1")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_one(post_repo, one_post, client, create_one_post):
    assert post_repo.all()
    response = client.delete(f"/post/{create_one_post.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not post_repo.get_one_or_none(id=create_one_post.id)


def test_patch_one(post_repo, one_post, client, create_one_post):
    assert post_repo.all()
    update_data = {"name": "string", "publication_date": "2023-08-17"}
    response = client.patch(f"/post/{create_one_post.id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    for key, val in update_data.items():
        assert data[key] == val


def test_pagination(create_five_post, client, post_repo):  # пареметризованные параметры
    assert post_repo.all()
    quantity = len(create_five_post)
    for j in range(1, quantity + 1):
        for i in range(1, ceil(quantity / j) + 1):
            response = client.get(f"post/?limit={j}&page={i}")
            assert response.status_code == HTTPStatus.OK
            data = response.json()
            assert data["total_pages"] == ceil(quantity / j)
            if i + 1 > ceil(quantity / j):
                assert data["next_page"] is None
            else:
                assert data["next_page"] == i + 1
            if i - 1 == 0:
                assert data["prev_page"] is None
            else:
                assert data["prev_page"] == i - 1


def test_sort(create_five_post, client, post_repo):
    assert post_repo.all()
    order_by = "image_url"
    response = client.get(f"post/?limit={len(create_five_post)}&order_by={order_by}")  # urllib
    assert response.status_code == HTTPStatus.OK
    sorted_list = sorted(create_five_post, key=itemgetter(order_by))
    data = response.json()["result"]
    for i in range(0, len(sorted_list)):
        for key, val in sorted_list[i].items():
            assert data[i][key] == val


def test_filter(create_five_post, client, post_repo):
    assert post_repo.all()
    filter_by = "image_url"
    filter_parametr = "https://mosday.ru/news/preview/446/4467714.jpg"
    response = client.get(f"post/?limit={len(create_five_post)}&{filter_by}={filter_parametr}")
    assert response.status_code == HTTPStatus.OK
    sorted_list = []
    for i in create_five_post:
        if i[filter_by] == filter_parametr:
            sorted_list.append(i)
    data = response.json()["result"]
    for i in range(0, len(sorted_list)):
        for key, val in sorted_list[i].items():
            assert data[i][key] == val
