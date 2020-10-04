from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


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


# class Restaurant(db.Model):
#     __tablename__ = "restaurant"
#
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
#     insert_datetime = db.Column(db.DateTime, server_default=func.now(), index=True)
#     name = db.Column(db.String, nullable=False, index=True)
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)
#     address = db.Column(db.String, nullable=False)
#     url = db.Column(db.String)
#
#     reviews = db.relationship("Review", lazy="select", back_populates="restaurant")
#
#     @hybrid_property
#     def slug(self):
#         return slugify(str(self.name))
#
#     @slug.expression
#     def slug(self):
#         return db.func.replace(
#             db.func.replace(db.func.lower(self.name), " ", "-"), ".", ""
#         )


# class Review(db.Model):
#     __tablename__ = "review"
#
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
#     insert_datetime = db.Column(db.DateTime, server_default=func.now(), index=True)
#     restaurant_id = db.Column(
#         db.Integer, db.ForeignKey("restaurant.id"), nullable=False, index=True
#     )
#     comment = db.Column(db.Text, nullable=False)
#
#     restaurant = db.relationship(
#         "Restaurant", uselist=False, lazy="joined", back_populates="reviews"
#     )
#
#     @hybrid_property
#     def restaurant_slug(self):
#         return slugify(self.restaurant.name)


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
