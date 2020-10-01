from flask import Blueprint

from .views import LoginView

auth = Blueprint("auth", __name__, url_prefix="/", template_folder="templates")

auth.add_url_rule(
    LoginView.rule, view_func=LoginView.as_view(LoginView.endpoint)
)
