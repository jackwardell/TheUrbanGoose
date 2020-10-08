import os
from unittest.mock import patch

import pytest
from tests.helpers import _get_csrf_from_form
from tests.helpers import login
from tests.helpers import OK_RESPONSE
from tests.helpers import restaurants

USERNAME = "hello"
PASSWORD = "world"

os.environ["USERNAME"] = USERNAME
os.environ["PASSWORD"] = PASSWORD


@pytest.fixture(scope="function")
def logged_in_client(client):
    login(client)
    return client


def test_admin_dashboard_redirect(client):
    resp = client.get("/admin/dashboard")
    assert resp.status_code == 302


def test_admin_dashboard_ok(logged_in_client):
    resp = logged_in_client.get("/admin/dashboard")
    assert resp.status_code == 200
    assert "/admin/find-restaurant" in resp.data.decode()
    assert "/admin/create-restaurant-review" in resp.data.decode()


def test_find_restaurant_redirect(client):
    resp = client.get("/admin/find-restaurant")
    assert resp.status_code == 302


def test_find_restaurant_ok(logged_in_client):
    resp = logged_in_client.get("/admin/find-restaurant")
    assert resp.status_code == 200


def test_create_restaurant_review_redirect(client):
    resp = client.get("/admin/create-restaurant-review")
    assert resp.status_code == 302


def test_create_restaurant_review_ok(logged_in_client):
    resp = logged_in_client.get("/admin/create-restaurant-review")
    assert resp.status_code == 200


def test_create_restaurant_review_works(logged_in_client):
    with patch("requests.get", return_value=OK_RESPONSE) as get:
        get_fields = ("address", "latitude", "longitude", "name")
        fields_seen_in_post = (
            "address",
            "name",
            "description",
            "cuisine",
            "price",
        )
        data = {
            "address": "St Pauls Cathedral, St Pauls Church Yard, London, England EC4M 8AE, United Kingdom",
            "latitude": -0.09837950000000001,
            "longitude": 51.513744,
            "name": "St Pauls Cathedral",
            "description": "Good church",
            "cuisine": "Word of The Lord",
            "price": "Free, actually maybe not? I do not know",
            "image_url": "https://www.image-goes-here.com/image.jpg",
            "menu_url": "https://www.menu-goes-here.com",
        }
        # quick check to keep me in line in case things change
        for field in get_fields:
            assert field in data
        for field in fields_seen_in_post:
            assert field in data

        resp = logged_in_client.get("/")
        for field in fields_seen_in_post:
            assert data[field] not in resp.data.decode()

        get_data = {k: v for k, v in data.items() if k in get_fields}
        resp = logged_in_client.get(
            "/admin/create-restaurant-review", query_string=get_data
        )
        assert resp.status_code == 200
        for value in get_data.values():
            assert str(value) in resp.data.decode()

        csrf_token = _get_csrf_from_form(resp.data.decode())
        data["csrf_token"] = csrf_token
        resp = logged_in_client.post(
            "/admin/create-restaurant-review", data=data
        )
        assert resp.status_code == 302
        assert resp.location == "http://localhost/"
        get.assert_called()

        resp = logged_in_client.get(resp.location)
        for field in fields_seen_in_post:
            assert data[field] in resp.data.decode()


def test_restaurant_reviews_redirect(client):
    resp = client.get("/admin/restaurant-reviews")
    assert resp.status_code == 302


def test_restaurant_reviews_ok(logged_in_client):
    resp = logged_in_client.get("/admin/restaurant-reviews")
    assert resp.status_code
    for restaurant in restaurants:
        assert restaurant["name"] in resp.data.decode()


@pytest.mark.parametrize("restaurant_id", [r["id"] for r in restaurants])
def test_restaurant_review_redirect(client, restaurant_id):
    resp = client.get(f"/admin/restaurant-review?id={restaurant_id}")
    assert resp.status_code == 302


@pytest.mark.parametrize("restaurant", restaurants)
def test_restaurant_review_ok(logged_in_client, restaurant):
    resp = logged_in_client.get(
        f"/admin/restaurant-review?id={restaurant['id']}"
    )
    assert resp.status_code == 200

    for field in [v for k, v in restaurant.items() if k != "insert_datetime"]:
        assert str(field) in resp.data.decode()


@pytest.mark.parametrize("query", ["", "?id=999"])
def test_restaurant_review_not_found(logged_in_client, query):
    resp = logged_in_client.get("/admin/restaurant-review" + query)
    assert resp.status_code == 404


@pytest.mark.parametrize("restaurant", restaurants)
def test_restaurant_review_update(logged_in_client, restaurant):
    resp = logged_in_client.get("/admin/restaurant-reviews")
    assert resp.data.decode().count("<tr>") == 4

    with patch("requests.get", return_value=OK_RESPONSE) as get:
        url = f"/admin/restaurant-review?id={restaurant['id']}"
        resp = logged_in_client.get(url)
        assert resp.status_code == 200

        data = {k: v for k, v in restaurant.items() if k != "insert_datetime"}
        for field in data.values():
            assert str(field) in resp.data.decode()

        name, address = "St. Nice place", "22 NEW ADDRESS BABY, SE99 420"
        assert name not in resp.data.decode()

        data["name"] = name
        data["address"] = address
        data["csrf_token"] = _get_csrf_from_form(resp.data.decode())
        data["update"] = True
        resp = logged_in_client.post(url, data=data)
        assert resp.status_code == 302
        assert resp.location == "http://localhost/admin/restaurant-reviews"

        resp = logged_in_client.get("/admin/restaurant-reviews")
        assert f"Successfully Updated: {name}" in resp.data.decode()
        assert restaurant["name"] not in resp.data.decode()
        assert name in resp.data.decode()
        assert resp.data.decode().count("<tr>") == 4
        get.assert_called()

        resp = logged_in_client.get(url)
        assert name in resp.data.decode()
        assert address in resp.data.decode()

        # adding this as when updating theres a bug that removed created time
        resp = logged_in_client.get("/")
        assert resp.status_code == 200


@pytest.mark.parametrize("restaurant", restaurants)
def test_restaurant_review_delete(logged_in_client, restaurant):
    resp = logged_in_client.get("/admin/restaurant-reviews")
    assert resp.data.decode().count("<tr>") == 4

    with patch("requests.get", return_value=OK_RESPONSE) as get:
        url = f"/admin/restaurant-review?id={restaurant['id']}"
        resp = logged_in_client.get(url)
        assert resp.status_code == 200

        data = {k: v for k, v in restaurant.items() if k != "insert_datetime"}
        data["csrf_token"] = _get_csrf_from_form(resp.data.decode())
        data["delete"] = True
        resp = logged_in_client.post(url, data=data)
        assert resp.status_code == 302
        assert resp.location == "http://localhost/admin/restaurant-reviews"

        resp = logged_in_client.get("/admin/restaurant-reviews")
        assert (
            f"Successfully Deleted: {restaurant['name']}" in resp.data.decode()
        )
        # re render to remove flash
        resp = logged_in_client.get("/admin/restaurant-reviews")
        assert restaurant["name"] not in resp.data.decode()
        assert resp.data.decode().count("<tr>") == 3
        get.assert_called()

        resp = logged_in_client.get(url)
        assert resp.status_code == 404
