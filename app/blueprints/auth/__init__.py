from flask import Blueprint

from .views import LoginView
from .views import LogoutView

auth = Blueprint("auth", __name__, url_prefix="/", template_folder="templates")

auth.add_url_rule(
    LoginView.rule, view_func=LoginView.as_view(LoginView.endpoint)
)

auth.add_url_rule(
    LogoutView.rule, view_func=LogoutView.as_view(LogoutView.endpoint)
)
