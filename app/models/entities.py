from datetime import datetime

import attr
from flask_login import UserMixin
from slugify import slugify


@attr.s
class User(UserMixin):
    username = attr.ib()
    password = attr.ib()

    def get_id(self):
        return self.username


@attr.s
class Review:
    restaurant = attr.ib()
    created = attr.ib()
    comment = attr.ib()

    @classmethod
    def from_form(cls, form):
        restaurant = Restaurant(
            name=form.restaurant.data,
            address=form.address.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            url=form.url.data,
        )
        post = cls(
            restaurant=restaurant,
            created=datetime.now(),
            comment=form.comment.data,
        )
        return post

    @classmethod
    def from_db(cls, model):
        restaurant = Restaurant(
            name=model.restaurant.name,
            address=model.restaurant.address,
            latitude=model.restaurant.latitude,
            longitude=model.restaurant.longitude,
            url=model.restaurant.url,
        )
        post = cls(
            restaurant=restaurant,
            created=model.insert_datetime,
            comment=model.comment,
        )
        return post

    @property
    def description(self):
        message = f"<strong>{self.restaurant.name}</strong><p><a href='{self.restaurant.url}' target='_blank'>Visit Site</a></p><p>{self.comment}</p>"
        return message

    def to_dict(self):
        rv = attr.asdict(self, recurse=True)
        rv["description"] = self.description
        rv["restaurant"]["slug"] = self.restaurant.slug
        return rv


@attr.s
class Restaurant:
    name = attr.ib()
    address = attr.ib()
    latitude = attr.ib()
    longitude = attr.ib()
    url = attr.ib()

    @property
    def slug(self):
        return slugify(self.name)
