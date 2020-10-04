import attr
from settings import PASSWORD
from settings import USERNAME

from .db import db
from .db import Restaurant as RestaurantModel
from .db import Review as ReviewModel
from .entities import Review as ReviewEntity
from .entities import User

__all__ = ["Repository", "db"]


@attr.s
class Repository:
    session = attr.ib(default=None)

    def init_db(self, db_session):
        self.session = db_session

    def save_review(self, review):
        # get restaurant by name if exists
        # todo: find out better thing to query than name
        restaurant = (
            self.session.query(RestaurantModel)
            .filter(
                db.func.lower(RestaurantModel.name)
                == db.func.lower(review.restaurant.name)
            )
            .first()
        )

        # if none, save one
        if restaurant is None:
            restaurant = RestaurantModel(
                name=review.restaurant.name,
                latitude=review.restaurant.latitude,
                longitude=review.restaurant.longitude,
                address=review.restaurant.address,
                url=review.restaurant.url,
            )
            self.session.add(restaurant)
            self.session.commit()

        # make review
        review = ReviewModel(
            restaurant_id=restaurant.id, comment=review.comment
        )
        self.session.add(review)
        self.session.commit()
        return review

    def get_all_reviews(self):
        rv = [
            ReviewEntity.from_db(review)
            for review in self.session.query(ReviewModel)
        ]
        return rv

    def get_user(self, username):
        return User(USERNAME, PASSWORD) if username == USERNAME else None

    def get_restaurant(self, slug):
        rv = self.session.query(RestaurantModel).filter(
            RestaurantModel.slug == slug
        )
        return rv.first()
