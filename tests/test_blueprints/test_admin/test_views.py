import os

from tests.helpers import _get_csrf_from_form

USERNAME = "hello"
PASSWORD = "world"

os.environ["USERNAME"] = USERNAME
os.environ["PASSWORD"] = PASSWORD


def test_admin_dashboard(admin_client):
    resp = admin_client.get("/admin/dashboard")
    assert resp.status_code == 200
    assert "/admin/find-restaurant" in resp.data.decode()
    assert "/admin/create-restaurant-review" in resp.data.decode()


def test_find_restaurant(admin_client):
    resp = admin_client.get("/admin/find-restaurant")
    assert resp.status_code == 200


def test_create_restaurant_review(admin_client):
    resp = admin_client.get("/admin/create-restaurant-review")
    assert resp.status_code == 200

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
        "image_url": "https://www.image-goes-here.com",
        "menu_url": "https://www.menu-goes-here.com",
    }
    # quick check to keep me in line in case things change
    for field in get_fields:
        assert field in data
    for field in fields_seen_in_post:
        assert field in data

    resp = admin_client.get("/")
    for field in fields_seen_in_post:
        assert data[field] not in resp.data.decode()

    get_data = {k: v for k, v in data.items() if k in get_fields}
    resp = admin_client.get(
        "/admin/create-restaurant-review", query_string=get_data
    )
    assert resp.status_code == 200
    for value in get_data.values():
        assert str(value) in resp.data.decode()

    csrf_token = _get_csrf_from_form(resp.data.decode())
    data["csrf_token"] = csrf_token
    resp = admin_client.post("/admin/create-restaurant-review", data=data)
    assert resp.status_code == 302
    assert resp.location == "http://localhost/"

    resp = admin_client.get(resp.location)
    for field in fields_seen_in_post:
        assert data[field] in resp.data.decode()
