from flask import request
from flask_wtf import FlaskForm
from settings import PASSWORD
from settings import USERNAME
from wtforms import BooleanField
from wtforms import FloatField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import ValidationError
from wtforms.validators import InputRequired


def validate_url(_, field):
    if not field.data.startswith("http"):
        raise ValidationError("A URL should start with http")


class RestaurantReviewForm(FlaskForm):
    restaurant = StringField(
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

    # tags = StringField("Tags")
    submit = SubmitField("Submit Review")

    # def parse_tags(self):
    #     rv = [
    #         tag.strip()[1:]
    #         for tag in self.tags.data.split(",")
    #         if tag.startswith("#")
    #     ]
    #     return rv


class FindRestaurantForm(FlaskForm):
    address = StringField(
        "Search Restaurant Address", validators=[InputRequired()]
    )
    restaurant = HiddenField("Restaurant", validators=[InputRequired()])
    latitude = HiddenField("Latitude", validators=[InputRequired()])
    longitude = HiddenField("Longitude", validators=[InputRequired()])
    submit = SubmitField("Find")


def validate_username(_, field):
    if field.data != USERNAME:
        raise ValidationError("Invalid username or password")


def validate_password(_, field):
    if field.data != PASSWORD:
        raise ValidationError("Invalid username or password")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), validate_username]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), validate_password]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")
