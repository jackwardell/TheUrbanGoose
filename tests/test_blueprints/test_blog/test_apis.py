from json import loads

import pytest
from flask.json import dumps


def _jsonify(data):
    return loads(dumps(data, indent=None, separators=(",", ":")))


def test_restaurant_api_all(client, restaurants):
    resp = client.get("/api/restaurants")
    assert resp.status_code == 200

    # alter restaurants fixture to make datetime like jsonify output
    assert resp.json == sorted(
        _jsonify(restaurants), key=lambda x: x["id"], reverse=True
    )


@pytest.mark.parametrize("restaurant_id", [1, 2, 3])
def test_restaurant_api_single(restaurant_id, client, restaurants):
    resp = client.get(f"/api/restaurants?id={restaurant_id}")
    assert resp.status_code == 200
    assert resp.json == _jsonify(
        [r for r in restaurants if r["id"] == restaurant_id].pop()
    )
