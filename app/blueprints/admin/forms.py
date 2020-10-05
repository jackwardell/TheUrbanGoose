from flask import request
from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms import HiddenField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import ValidationError
from wtforms.validators import InputRequired


def validate_url(_, field):
    if not field.data.startswith("http"):
        raise ValidationError("A URL should start with http")


class RestaurantReviewForm(FlaskForm):
    name = StringField(
        "Restaurant",
        default=lambda: request.args.get("restaurant"),
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
        "Image URL", validators=[InputRequired(), validate_url]
    )

    submit = SubmitField("Submit Review")


class FindRestaurantForm(FlaskForm):
    address = StringField(
        "Search Restaurant Address", validators=[InputRequired()]
    )
    restaurant = HiddenField("Restaurant", validators=[InputRequired()])
    latitude = HiddenField("Latitude", validators=[InputRequired()])
    longitude = HiddenField("Longitude", validators=[InputRequired()])
    submit = SubmitField("Find")
