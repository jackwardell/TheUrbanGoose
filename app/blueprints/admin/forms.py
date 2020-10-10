import requests
from app.static import FoodOrDrink
from flask import request
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import Field
from wtforms import FloatField
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import ValidationError
from wtforms.validators import InputRequired
from wtforms.widgets import HiddenInput
from wtforms.widgets import TextInput


def validate_url(_, field):
    # if not field.data.startswith("http"):
    #     raise ValidationError("A URL should start with http")
    # else:
    r = requests.get(field.data)
    if str(r.status_code).startswith(("4", "5")):
        raise ValidationError("A URL should be valid")


# def validate_is_image(_, field):
#     import mimetypes
#     from urllib.parse import urlparse
#     mimetype, _ = mimetypes.guess_type(urlparse(field.data).path)
#     if not (mimetype and mimetype.startswith("image")):
#         raise ValidationError("A image URL must contain an image")


# def validate_tags(_, field):
#     [i.trim().lower() for i in field.data.split(",")]


class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return ", ".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip().lower() for x in valuelist[0].split(",")]
        else:
            self.data = []


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
    description = TextAreaField(
        "Description",
        default=lambda: request.args.get("description"),
        validators=[InputRequired()],
    )
    cuisine = StringField(
        "Cuisine Type",
        default=lambda: request.args.get("cuisine"),
        validators=[InputRequired()],
    )
    price = StringField(
        "Price",
        default=lambda: request.args.get("price"),
        validators=[InputRequired()],
    )
    menu_url = StringField(
        "Menu URL",
        default=lambda: request.args.get("menu_url"),
        validators=[InputRequired(), validate_url],
    )
    image_url = StringField(
        "Image URL",
        default=lambda: request.args.get("image_url"),
        validators=[
            InputRequired(),
            validate_url,
            # validate_is_image
        ],
    )
    food_or_drink = SelectField(
        "For Food, Drink or Both?",
        choices=[FoodOrDrink.FOOD, FoodOrDrink.DRINK, FoodOrDrink.BOTH],
        validators=[InputRequired()],
    )
    tags = TagListField("Good For")

    @property
    def for_food(self):
        return self.food_or_drink.data == FoodOrDrink.FOOD or self.for_both

    @property
    def for_drink(self):
        return self.food_or_drink.data == FoodOrDrink.DRINK or self.for_both

    @property
    def for_both(self):
        return self.food_or_drink.data == FoodOrDrink.BOTH

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
            "for_food": self.for_food,
            "for_drink": self.for_drink,
            "tags": self.tags.data,
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

    is_archived = BooleanField(
        "Is Archived?",
        validators=[InputRequired()],
        widget=HiddenInput(),
        default=lambda: request.args.get("is_archived"),
    )
    archive = SubmitField("Archive Review")
    unarchive = SubmitField("Unarchive Review")

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
