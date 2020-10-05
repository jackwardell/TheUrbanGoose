import os
import tempfile
from datetime import datetime
from json import loads

import pytest
from flask.json import dumps

from .helpers import _get_csrf_from_form
from .helpers import PASSWORD
from .helpers import USERNAME


@pytest.fixture(scope="session")
def restaurants():
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
    return restaurants


@pytest.fixture(scope="function")
def client(restaurants):
    from app import create_app
    from app import db

    app = create_app()

    with app.test_client() as testing_client:
        with app.app_context():
            db_file_directory, db_file = tempfile.mkstemp()
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_file
            app.config["TESTING"] = True

            db.create_all()

            from app.models import Restaurant

            for restaurant in restaurants:
                db.session.add(Restaurant(**restaurant))

            db.session.commit()

            yield testing_client

            os.close(db_file_directory)


@pytest.fixture(scope="function")
def admin_client(client):
    resp = client.get("/login")
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
    return client


@pytest.fixture(scope="session")
def _jsonify():
    return lambda data: loads(dumps(data, indent=None, separators=(",", ":")))
