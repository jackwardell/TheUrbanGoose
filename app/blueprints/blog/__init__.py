from flask import Blueprint

from .apis import LocationsAPI
from .views import HomeView

blog = Blueprint("blog", __name__, url_prefix="/", template_folder="templates")

blog.add_url_rule(HomeView.rule, view_func=HomeView.as_view(HomeView.endpoint))
blog.add_url_rule(
    LocationsAPI.rule, view_func=LocationsAPI.as_view(LocationsAPI.endpoint)
)
