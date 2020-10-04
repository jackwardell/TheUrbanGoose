from flask_wtf import FlaskForm
from settings import PASSWORD
from settings import USERNAME
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import ValidationError
from wtforms.validators import InputRequired


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
