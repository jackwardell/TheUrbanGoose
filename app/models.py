from datetime import datetime

import attr
from app.static import FoodOrDrink
from app.static import QueryOrder
from app.utils import get_food_and_or_drink
from flask import request
from flask import session
from flask_login import AnonymousUserMixin
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from settings import PASSWORD
from settings import USERNAME
from sqlalchemy import func
from werkzeug.http import http_date
from werkzeug.urls import url_encode

db = SQLAlchemy()


@attr.s
class Repository:
    session = attr.ib(default=None)

    def init_db(self, db_session):
        self.session = db_session

    def save_restaurant(self, restaurant):
        self.session.add(restaurant)
        self.session.commit()
        return restaurant

    def update_restaurant(self, restaurant):
        old_restaurant = self.get_restaurant(restaurant.id)
        for k, v in restaurant.to_dict().items():
            if getattr(old_restaurant, k) != v and k != "insert_datetime":
                setattr(old_restaurant, k, v)
        self.session.commit()
        return restaurant

    def get_restaurants(
        self,
        order: str = QueryOrder.DESC,
        active: bool = True,
        archived: bool = False,
        food_or_drink: str = FoodOrDrink.EITHER,
    ):
        q = self.session.query(Restaurant)

        if active is False and archived is False:
            raise ValueError("you must have either active or archived")
        elif active is True and archived is False:
            q = q.filter_by(is_archived=False)
        elif active is False and archived is True:
            q = q.filter_by(is_archived=True)

        if food_or_drink not in FoodOrDrink.CHOICES:
            raise ValueError(
                f"food_or_drink must be in ({FoodOrDrink.CHOICES}) "
                f"not {food_or_drink}"
            )
        if food_or_drink == FoodOrDrink.FOOD:
            q = q.filter_by(for_food=True)
        elif food_or_drink == FoodOrDrink.DRINK:
            q = q.filter_by(for_drink=True)
        elif food_or_drink == FoodOrDrink.BOTH:
            q = q.filter_by(for_drink=True).filter_by(for_food=True)

        if order.lower() == QueryOrder.DESC:
            q = q.order_by(Restaurant.insert_datetime.desc())
        elif order.lower() == QueryOrder.ASC:
            q = q.order_by(Restaurant.insert_datetime)
        else:
            raise ValueError("order must be asc or desc")

        return q.all()

    def get_restaurant(self, *restaurant_id, **fields):
        if restaurant_id:
            return self.session.query(Restaurant).get(restaurant_id[0])
        else:
            q = self.session.query(Restaurant)
            for k, v in fields.items():
                q = q.filter_by(**{k: v})
            return q.one()

    def archive_restaurant(self, restaurant):
        restaurant.is_archived = True
        self.session.commit()

    def unarchive_restaurant(self, restaurant):
        restaurant.is_archived = False
        self.session.commit()

    def delete_restaurant(self, restaurant):
        self.session.delete(restaurant)
        self.session.commit()
        return restaurant.name

    def list_all_tags(self):
        return

    def record_page_view(self, page_view):
        self.session.add(page_view)
        self.session.commit()

    @staticmethod
    def get_user(username):
        return User(USERNAME, PASSWORD) if username == USERNAME else None


class RequesterMixin:
    @property
    def ip_address(self):
        return request.remote_addr

    @property
    def name(self):
        return session.get("name")


class User(UserMixin, RequesterMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username


class Anon(AnonymousUserMixin, RequesterMixin):
    pass


class PageView(db.Model):
    __tablename__ = "page_view"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, index=True
    )
    insert_datetime = db.Column(
        db.DateTime, server_default=func.now(), index=True
    )
    ip_address = db.Column(db.String, nullable=False)
    method = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    query = db.Column(db.String)
    status_code = db.Column(db.String, nullable=False)

    @property
    def date(self):
        return http_date(self.insert_datetime.timestamp())

    @property
    def url(self):
        return self.path + "?" + self.query if self.query else self.path

    @classmethod
    def from_response(cls, response):
        from flask import request
        from flask_login import current_user

        page_view = PageView(
            insert_datetime=datetime.now(),
            ip_address=current_user.ip_address,
            method=request.method,
            path=request.path,
            query=request.query_string.decode(),
            status_code=response.status_code,
        )
        return page_view

    def to_dict(self):
        rv = {
            "id": self.id,
            "insert_datetime": self.insert_datetime,
            "ip_address": self.ip_address,
            "method": self.method,
            "path": self.path,
            "query": self.query,
            "status_code": self.status_code,
        }
        return rv

    def __str__(self):
        return f'{self.ip_address} @ [{self.date}] - "{self.method}: {self.url}" - {self.status_code}'


restaurant_tag_association = db.Table(
    "restaurant_tag_association",
    db.Model.metadata,
    db.Column("restaurant_id", db.Integer, db.ForeignKey("restaurant.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
)


# class RestaurantTagAssociation(db.Model):
#     __tablename__ = "restaurant_tag_association"
#
#     restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), primary_key=True)
#     tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)
#
#     # __table_args__ = (db.ForeignKeyConstraint(""),)
#
#     restaurant = db.relationship("Restaurant", back_populates="tags")
#     tag = db.relationship("Tag", back_populates="restaurants")


class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, index=True
    )
    insert_datetime = db.Column(
        db.DateTime, server_default=func.now(), index=True
    )
    name = db.Column(db.String, nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    cuisine = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    # nullable for now -- see what alex thinks
    menu_url = db.Column(db.String)
    image_url = db.Column(db.String)
    for_food = db.Column(db.Boolean, default=True, nullable=False)
    for_drink = db.Column(db.Boolean, default=True, nullable=False)
    is_archived = db.Column(db.Boolean, default=False, nullable=False)

    tags = db.relationship(
        # "RestaurantTagAssociation",
        "Tag",
        secondary="restaurant_tag_association",
        back_populates="restaurants",
    )

    @property
    def date(self):
        return http_date(self.insert_datetime.timestamp())

    def formatted_tags(self):
        tags = [tag.name for tag in self.tags if tag is not None]
        if tags:
            comma_separated, and_separated = tags[:-1], tags[-1]
            if comma_separated:
                return ", ".join(comma_separated) + " and " + and_separated
            else:
                return and_separated
        else:
            return "Everything"

    @classmethod
    def from_form(cls, form):
        params = form.to_dict()
        params.setdefault("is_archived", False)
        tags = params.pop("tags", [])
        tags = [Tag(name=tag) for tag in tags if tag != ""]
        restaurant = Restaurant(**params)
        if tags:
            restaurant.tags.extend(tags)
        return restaurant

    @property
    def food_or_drink(self):
        return get_food_and_or_drink(
            for_drink=self.for_drink, for_food=self.for_food
        )

    def to_dict(self):
        rv = {
            "id": self.id,
            "insert_datetime": self.insert_datetime,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "description": self.description,
            "cuisine": self.cuisine,
            "price": self.price,
            "menu_url": self.menu_url,
            "image_url": self.image_url,
            "for_food": self.for_food,
            "for_drink": self.for_drink,
            "is_archived": self.is_archived,
        }
        return rv

    def query_string(self):
        return "/admin/create-restaurant-review?" + url_encode(self.to_dict())


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, index=True
    )
    insert_datetime = db.Column(
        db.DateTime, server_default=func.now(), nullable=False
    )
    name = db.Column(db.String, nullable=False, index=True)

    restaurants = db.relationship(
        # "RestaurantTagAssociation",
        "Restaurant",
        secondary="restaurant_tag_association",
        back_populates="tags",
    )
