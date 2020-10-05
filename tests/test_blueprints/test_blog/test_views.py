from tests.helpers import restaurants


def test_home_view(client):
    resp = client.get("/")
    assert resp.status_code == 200

    for restaurant in restaurants:
        assert restaurant["name"] in resp.data.decode()
        assert restaurant["cuisine"] in resp.data.decode()
        assert restaurant["description"] in resp.data.decode()
        assert restaurant["price"] in resp.data.decode()
