def test_home_view(client, restaurants):
    resp = client.get("/")
    assert resp.status_code == 200

    for restaurant in restaurants:
        assert restaurant["name"] in resp.data.decode()
        assert restaurant["cuisine"] in resp.data.decode()
        assert restaurant["description"] in resp.data.decode()
        assert restaurant["price"] in resp.data.decode()
