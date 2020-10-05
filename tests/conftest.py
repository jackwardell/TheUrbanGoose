import os
import tempfile

import pytest

from .helpers import _get_csrf_from_form
from .helpers import PASSWORD
from .helpers import restaurants
from .helpers import USERNAME


@pytest.fixture(scope="function")
def client():
    db_file_directory, db_file = tempfile.mkstemp()

    os.environ["SQLALCHEMY_URL"] = "sqlite:///" + db_file

    from app import create_app
    from app import db

    app = create_app()

    with app.test_client() as testing_client:
        with app.app_context():
            app.config["SQLALCHEMY_DATABASE_URI"] = os.environ[
                "SQLALCHEMY_URL"
            ]
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
