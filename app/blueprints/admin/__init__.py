from flask import Blueprint

from .apis import LocationAPI
from .views import AdminDashboardView
from .views import CreateReviewView
from .views import FindRestaurantView

# from .apis import TagAPI

admin = Blueprint(
    "admin", __name__, url_prefix="/admin", template_folder="templates"
)

admin.add_url_rule(
    FindRestaurantView.rule,
    view_func=FindRestaurantView.as_view(FindRestaurantView.endpoint),
)
admin.add_url_rule(
    CreateReviewView.rule,
    view_func=CreateReviewView.as_view(CreateReviewView.endpoint),
)
admin.add_url_rule(
    AdminDashboardView.rule,
    view_func=AdminDashboardView.as_view(AdminDashboardView.endpoint),
)
# admin.add_url_rule(TagAPI.rule, view_func=TagAPI.as_view(TagAPI.endpoint))
admin.add_url_rule(
    LocationAPI.rule, view_func=LocationAPI.as_view(LocationAPI.endpoint)
)
