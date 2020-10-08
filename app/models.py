from datetime import datetime

import attr
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

    def get_all_restaurants(self, order="desc"):
        if order.lower() == "desc":
            order_by = Restaurant.insert_datetime.desc()
        elif order.lower() == "asc":
            order_by = Restaurant.insert_datetime
        else:
            raise ValueError("order must be asc or desc")
        return self.session.query(Restaurant).order_by(order_by).all()

    def get_restaurant(self, *restaurant_id, **fields):
        if restaurant_id:
            return self.session.query(Restaurant).get(restaurant_id[0])
        else:
            q = self.session.query(Restaurant)
            for k, v in fields.items():
                q = q.filter_by(**{k: v})
            return q.one()

    def delete_restaurant(self, restaurant):
        self.session.delete(restaurant)
        self.session.commit()
        return restaurant.name

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
    # good_for = db.Column(db.String, nullable=False)
    # nullable for now -- see what alex thinks
    menu_url = db.Column(db.String)
    image_url = db.Column(db.String)

    @property
    def date(self):
        return http_date(self.insert_datetime.timestamp())

    @classmethod
    def from_form(cls, form):
        restaurant = Restaurant(**form.to_dict())
        return restaurant

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
        }
        return rv

    def query_string(self):
        return "/admin/create-restaurant-review" + url_encode(self.to_dict())

    # def to_slack(self):
    #     import json
    #     message = f"```{json.dumps(self.to_dict(), indent=4,}```"
    #     return


# class PageHit(db.Model):
#     __tablename__ = "page_hit"
#
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
#     insert_datetime = db.Column(db.DateTime, server_default=func.now(), index=True)
#     ip_address = db.Column(db.String)
#     url = db.Column(db.String, nullable=False)
#     user = db.Column(db.String)
#     status_code = db.Column(db.Integer, nullable=False)
#
#     def to_dict(self):
#         data = {
#             "id": self.id,
#             "datetime": self.insert_datetime,
#             "ip_address": self.ip_address,
#             "url": self.url,
#         }
#         return data
#
#     def __str__(self):
#         return f"{self.id}: {self.ip_address} @ {self.insert_datetime} on {self.url} as {self.user}"
#
#     # def to_slack(self):
#     #     client = get_slack_time()
#     #     return client.chat.post_message("page-hits", str(self))

# class Tag(db.Model,DateTimeMixin):
#     __tablename__ = "tag"
#
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
#     insert_datetime = db.Column(db.DateTime, server_default=func.now(), index=True)
#     name = db.Column(db.String, nullable=False, index=True)


# class TagReviewAssociation(db.Model, DateTimeMixin):
#     __tablename__ = "tag_review_association"
#
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
#     insert_datetime = db.Column(db.DateTime, server_default=func.now(), index=True)
#     tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False, index=True)
#     review_id = db.Column(
#         db.Integer, db.ForeignKey("review.id"), nullable=False, index=True
#     )
# class DateTime:
#     def __init__(self, datetime):
#         self._datetime = datetime
#
#     @classmethod
#     def now(cls):
#         return cls(datetime.now())
#
#     def __str__(self):
#         return self._datetime.strftime("%d %b %Y")
#
#
# class DateTimeMixin:
#     @property
#     def insert_datetime(self):
#         raise NotImplementedError()
#
#     @property
#     def date(self):
#         return DateTime(self.insert_datetime)
