from app.flask_simpleview import Group

from .apis import RestaurantAPI
from .views import HomeView

blog = Group("blog", __name__, url_prefix="/", template_folder="templates")

blog.add_view(HomeView)
blog.add_api(RestaurantAPI)
