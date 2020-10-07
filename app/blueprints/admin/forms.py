import mimetypes

import requests
from flask import request
from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import ValidationError
from wtforms.validators import InputRequired
from wtforms.widgets import HiddenInput


def validate_url(_, field):
    if not field.data.startswith("http"):
        raise ValidationError("A URL should start with http")
    else:
        r = requests.get(field.data)
        if r.status_code != 200:
            raise ValidationError("A URL should be valid")


def validate_is_image(_, field):
    mimetype, _ = mimetypes.guess_type(field.data)
    if not (mimetype and mimetype.startswith("image")):
        raise ValidationError("A image URL must contain an image")


class RestaurantReviewBase(FlaskForm):
    name = StringField(
        "Name",
        default=lambda: request.args.get("name"),
        validators=[InputRequired()],
    )
    latitude = FloatField(
        "Latitude",
        default=lambda: request.args.get("latitude"),
        validators=[InputRequired()],
    )
    longitude = FloatField(
        "Longitude",
        default=lambda: request.args.get("longitude"),
        validators=[InputRequired()],
    )
    address = StringField(
        "Address",
        default=lambda: request.args.get("address"),
        validators=[InputRequired()],
    )
    description = TextAreaField("Description", validators=[InputRequired()])
    cuisine = StringField("Cuisine Type", validators=[InputRequired()])
    price = StringField("Price", validators=[InputRequired()])
    menu_url = StringField(
        "Menu URL", validators=[InputRequired(), validate_url]
    )
    image_url = StringField(
        "Image URL",
        validators=[InputRequired(), validate_url, validate_is_image],
    )

    def to_dict(self):
        rv = {
            "name": self.name.data,
            "latitude": self.latitude.data,
            "longitude": self.longitude.data,
            "address": self.address.data,
            "description": self.description.data,
            "cuisine": self.cuisine.data,
            "price": self.price.data,
            "menu_url": self.menu_url.data,
            "image_url": self.image_url.data,
        }
        return rv


class CreateRestaurantReviewForm(RestaurantReviewBase):
    create = SubmitField("Submit Review")


class UpdateOrDeleteRestaurantReviewForm(RestaurantReviewBase):
    id = IntegerField(
        "ID",
        validators=[InputRequired()],
        widget=HiddenInput(),
        default=lambda: request.args.get("restaurant_id"),
    )
    update = SubmitField("Update Review")
    delete = SubmitField("Delete Review")

    def to_dict(self):
        rv = super().to_dict()
        rv["id"] = self.id.data
        return rv


class FindRestaurantForm(FlaskForm):
    address = StringField(
        "Search Restaurant Address", validators=[InputRequired()]
    )
    name = HiddenField("Restaurant", validators=[InputRequired()])
    latitude = HiddenField("Latitude", validators=[InputRequired()])
    longitude = HiddenField("Longitude", validators=[InputRequired()])
    submit = SubmitField("Find")
