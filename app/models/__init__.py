import attr
from settings import PASSWORD
from settings import USERNAME

from .db import db
from .db import Restaurant
from .entities import User

# from .db import Review as ReviewModel
# from .entities import Review as ReviewEntity

__all__ = ["Repository", "db"]


@attr.s
class Repository:
    session = attr.ib(default=None)

    def init_db(self, db_session):
        self.session = db_session

    def save_restaurant(self, restaurant):
        restaurant = Restaurant(
            name=restaurant.name,
            latitude=restaurant.latitude,
            longitude=restaurant.longitude,
            address=restaurant.address,
            description=restaurant.description,
            cuisine=restaurant.cuisine,
            price=restaurant.price,
            menu_url=restaurant.menu_url,
            image_url=restaurant.image_url,
        )

        self.session.add(restaurant)
        self.session.commit()
        return restaurant

    def get_all_reviews(self):
        return self.session.query(Restaurant).all()

    def get_user(self, username):
        return User(USERNAME, PASSWORD) if username == USERNAME else None

    def get_restaurant(self, **fields):
        q = self.session.query(Restaurant)
        for k, v in fields.items():
            q = q.filter_by(**{k: v})
        return q.one()
