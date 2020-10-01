from flask import request
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import FloatField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import InputRequired


class CreateReviewForm(FlaskForm):
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
    url = StringField("URL", validators=[InputRequired()])
    comment = TextAreaField("Comment", validators=[InputRequired()])
    tags = StringField("Tags")
    submit = SubmitField("Submit Review")

    def parse_tags(self):
        rv = [
            tag.strip()[1:]
            for tag in self.tags.data.split(",")
            if tag.startswith("#")
        ]
        return rv


class FindRestaurantForm(FlaskForm):
    address = StringField(
        "Search Restaurant Address", validators=[InputRequired()]
    )
    restaurant = HiddenField("Restaurant", validators=[InputRequired()])
    latitude = HiddenField("Latitude", validators=[InputRequired()])
    longitude = HiddenField("Longitude", validators=[InputRequired()])
    submit = SubmitField("Find")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")
