import os
from datetime import datetime
from json import loads

from flask.json import dumps

os.environ["GOOSE_ENV"] = GOOSE_ENV = "production"
os.environ["USERNAME"] = USERNAME = "hello"
os.environ["PASSWORD"] = PASSWORD = "world"

os.environ["SLACK_API_TOKEN"] = "xoxo-slack-api-token"
os.environ["SECRET_KEY"] = "not-so-secret"


def _jsonify(data):
    return loads(dumps(data, indent=None, separators=(",", ":")))


restaurants = [
    {
        "id": 1,
        "address": "St. John Bar and Restaurant, 26 St. John St, London, England EC1M 4AY, United Kingdom",
        "cuisine": "Nose to tail",
        "description": "AMAZING",
        "image_url": "https://www.allinlondon.co.uk/images/venues/images_all/13186455.jpg",
        "insert_datetime": datetime.fromtimestamp(1601906000),
        "latitude": -0.101382,
        "longitude": 51.520437,
        "menu_url": "https://stjohnrestaurant.com/a/restaurants/smithfield",
        "name": "St. John Bar and Restaurant",
        "price": "£70 a head",
    },
    {
        "id": 2,
        "address": "Prince of Peckham, London, England SE15 5EG, United Kingdom",
        "cuisine": "Jerk meat, roasts and chips",
        "description": "Anything jerk is highly recommended ",
        "image_url": "https://princeofpeckham.co.uk/wp-content/uploads/2019/10/MA_723A5044-720x530.jpg",
        "insert_datetime": datetime.fromtimestamp(1601907000),
        "latitude": -0.065532,
        "longitude": 51.473755,
        "menu_url": "https://princeofpeckham.co.uk/food-and-drink/",
        "name": "Prince of Peckham",
        "price": "Very reasonable, only \u00a320 for a full stomach ",
    },
    {
        "id": 3,
        "address": "Falafel And Shawarma, London, England SE5 8TS, United Kingdom",
        "cuisine": "Falafel andKebab",
        "description": "Amazing chicken shawarma and lamb sambusak ",
        "image_url": "https://www.allinlondon.co.uk/images/venues/images_all/13186455.jpg",
        "insert_datetime": datetime.fromtimestamp(1601908000),
        "latitude": -0.090308,
        "longitude": 51.474045,
        "menu_url": "https://www.zomato.com/london/falafel-shawarma-camberwell",
        "name": "Falafel And Shawarma",
        "price": "Cheap, \u00a35 for a full stomach!",
    },
]


def _get_csrf_from_form(html):
    input_tag = html.split('<div class="form-group">')[1].split(
        "</div>", maxsplit=1
    )[0]
    value = input_tag[input_tag.find("value=") :]
    token = value.split('"')[1]
    # check its a long string
    assert len(token) > 80
    return token
