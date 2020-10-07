from app.flask_simpleview import Group

from .apis import LocationAPI
from .views import AdminDashboardView
from .views import CreateRestaurantReviewView
from .views import FindRestaurantView
from .views import RestaurantReview
from .views import RestaurantReviewsView

admin = Group(
    "admin", __name__, url_prefix="/admin", template_folder="templates"
)

admin.add_view(FindRestaurantView)
admin.add_view(CreateRestaurantReviewView)
admin.add_view(AdminDashboardView)
admin.add_view(RestaurantReviewsView)
admin.add_view(RestaurantReview)

admin.add_api(LocationAPI)
