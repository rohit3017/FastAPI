import pytest
from app import models, schemas
from fastapi import HTTPException


def test_get_all_post(authorized_client, test_post):
    res = authorized_client.get("/posts/")

    def create_post_model(post_data):
        return schemas.PostOut(**post_data)

    posts = list(map(create_post_model, res.json()))

    assert len(posts) == len(test_post)

    assert res.status_code == 200


def test_unauthorized_user_get_one_post(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401


def test_unauthorized_user_get_all_post(client):
    res = client.get(f"/posts/")
    assert res.status_code == 401


def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")

    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_post[0].id
    assert post.Post.title == test_post[0].title
    assert post.Post.content == test_post[0].content
    assert res.status_code == 200


def test_get_one_post_not_exist(authorized_client):
    res = authorized_client.get(f"/posts/{9999999}")
    assert res.json()["detail"] == f"post with id {9999999} does not exist"
    assert res.status_code == 404


@pytest.mark.parametrize(
    "title,content,published",
    [
        ("awesome title", "awesome content", True),
        ("Favorite Pizza", "Indi Tandori", False),
        ("my title", "demo content", True),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title": "good title", "content": "good content"}
    )
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "good title"
    assert created_post.content == "good content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_create_post(client):
    res = client.get(
        f"/posts/", json={"title": "good fndhggu", "content": "good dfdhfhgjgbb"}
    )
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204


def test_delete_post_does_not_exist(authorized_client):
    res = authorized_client.delete(f"/posts/{8888888}")
    assert res.status_code == 404


def test_delete_post_other_user(authorized_client, test_post):
    res = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert res.status_code


def test_unauthorized_update_post(client, test_post):
    res = client.put(
        f"/posts/{test_post[0].id}",
        json={"title": "updated title", "content": "updated content"},
    )
    assert res.status_code == 401


def test_update_post(authorized_client, test_post):
    res = authorized_client.put(
        f"/posts/{test_post[0].id}",
        json={"title": "updated title", "content": "updated content"},
    )
    post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert post.title == "updated title"
    assert post.content == "updated content"


def test_update_post_does_not_exist(authorized_client):
    res = authorized_client.put(
        f"/posts/{999999}", json={"title": "test title", "content": "test content"}
    )
    assert res.status_code == 404


def test_update_post_another_user(authorized_client, test_post):
    res = authorized_client.put(
        f"/posts/{test_post[3].id}",
        json={"title": "test title", "content": "test content"},
    )
    assert res.status_code == 403
