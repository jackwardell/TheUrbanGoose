from unittest.mock import patch

QUERY_TERM = "St. John"
QUERY_RESULT = [
    {
        "address": "St. John Bread and Wine, 94-96 Commercial St, London, England E1 6BG, United Kingdom",
        "latitude": -0.07453,
        "longitude": 51.519768,
        "name": "St. John Bread and Wine",
    },
    {
        "address": "St. John Bar and Restaurant, 26 St. John St, London, England EC1M 4AY, United Kingdom",
        "latitude": -0.101382,
        "longitude": 51.520437,
        "name": "St. John Bar and Restaurant",
    },
    {
        "address": "St John Bakery, 72 Druid St, London, England SE1 3FH, United Kingdom",
        "latitude": -0.075524,
        "longitude": 51.499326,
        "name": "St John Bakery",
    },
    {
        "address": "St. John's Gate, 26 St John's Ln, London, England EC1M 4PP, United Kingdom",
        "latitude": -0.1027655,
        "longitude": 51.5218925,
        "name": "St. John's Gate",
    },
    {
        "address": "St John The Evangelist, Waterloo Rd, London, England SE1 8TY, United Kingdom",
        "latitude": -0.112329,
        "longitude": 51.504386,
        "name": "St John The Evangelist",
    },
    {
        "address": "St John's Blackheath, Stratheden Road, London, England SE3 7JH, United Kingdom",
        "latitude": 0.018677,
        "longitude": 51.4757535,
        "name": "St John's Blackheath",
    },
    {
        "address": "St. John's Church, Church Grove, Hampton Wick, Kingston Upon Thames, England KT1 4AN, United Kingdom",
        "latitude": -0.312706,
        "longitude": 51.411907,
        "name": "St. John's Church",
    },
    {
        "address": "St John's Tavern, 91 Junction Rd., London, England N19 5QX, United Kingdom",
        "latitude": -0.135732,
        "longitude": 51.562924,
        "name": "St John's Tavern",
    },
    {
        "address": "St. John Bakery, 3 Neal's Yard, London, England WC2H 9ER, United Kingdom",
        "latitude": -0.12641,
        "longitude": 51.514435,
        "name": "St. John Bakery",
    },
    {
        "address": "St. John's Wood Road Baptist Church, 39 St. John's Wood Road, London, England NW8 8UL, United Kingdom",
        "latitude": -0.17533300000000002,
        "longitude": 51.527120499999995,
        "name": "St. John's Wood Road Baptist Church",
    },
]

QUERY = (QUERY_TERM, QUERY_RESULT)


@patch("app.blueprints.admin.apis.search_location", return_value=QUERY_RESULT)
def test_location_api(search_location, client, _jsonify):
    resp = client.get(f"/admin/api/location?q={QUERY_TERM}")
    assert resp.status_code == 200
    # alter restaurants fixture to make datetime like jsonify output
    assert resp.json == _jsonify(QUERY_RESULT)
    search_location.assert_called_once_with(QUERY_TERM)
