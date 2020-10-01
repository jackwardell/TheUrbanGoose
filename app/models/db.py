from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class DateTime:
    def __init__(self, datetime):
        self._datetime = datetime

    @classmethod
    def now(cls):
        return cls(datetime.now())

    def __str__(self):
        return self._datetime.strftime("%d %b %Y")


class DateTimeMixin:
    @property
    def insert_datetime(self):
        raise NotImplementedError()

    @property
    def date(self):
        return DateTime(self.insert_datetime)


class PageHit(db.Model, DateTimeMixin):
    __tablename__ = "page_hit"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, index=True
    )
    insert_datetime = db.Column(
        db.DateTime, server_default=func.now(), index=True
    )
    ip_address = db.Column(db.String)
    url = db.Column(db.String, nullable=False)
    user = db.Column(db.String)
    status_code = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        data = {
            "id": self.id,
            "datetime": self.date,
            "ip_address": self.ip_address,
            "url": self.url,
        }
        return data

    def __str__(self):
        return f"{self.id}: {self.ip_address} @ {self.insert_datetime} on {self.url} as {self.user}"

    # def to_slack(self):
    #     client = get_slack_time()
    #     return client.chat.post_message("page-hits", str(self))


class Restaurant(db.Model, DateTimeMixin):
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
    url = db.Column(db.String)

    reviews = db.relationship(
        "Review", lazy="select", back_populates="restaurant"
    )


class Review(db.Model, DateTimeMixin):
    __tablename__ = "review"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, index=True
    )
    insert_datetime = db.Column(
        db.DateTime, server_default=func.now(), index=True
    )
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id"), nullable=False, index=True
    )
    comment = db.Column(db.Text, nullable=False)

    restaurant = db.relationship(
        "Restaurant", uselist=False, lazy="joined", back_populates="reviews"
    )


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
