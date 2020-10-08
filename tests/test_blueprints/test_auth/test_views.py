from tests.helpers import _get_csrf_from_form
from tests.helpers import login
from tests.helpers import PASSWORD
from tests.helpers import USERNAME


def test_login(client):
    resp = client.get("/admin/dashboard")
    assert resp.status_code == 302
    assert resp.location == "http://localhost/login?next=%2Fadmin%2Fdashboard"

    resp = client.get("/login")
    assert resp.status_code == 200

    csrf_token = _get_csrf_from_form(resp.data.decode())
    resp = client.post(
        "/login",
        data={
            "csrf_token": csrf_token,
            "username": USERNAME,
            "password": PASSWORD,
        },
    )
    assert resp.status_code == 302
    assert resp.location == "http://localhost/admin/dashboard"

    resp = client.get("/login")
    assert resp.status_code == 302
    assert resp.location == "http://localhost/admin/dashboard"


def test_logout_redirect(client):
    resp = client.get("/logout")
    assert resp.status_code == 302
    assert resp.location == "http://localhost/login?next=%2Flogout"


def test_logout_ok(client):
    login(client)
    resp = client.get("/logout")
    assert resp.status_code == 302
    assert resp.location == "http://localhost/"
