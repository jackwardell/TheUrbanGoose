from app import repo
from app.flask_simpleview import View
from app.static import FoodOrDrink


class HomeView(View):
    rule = "/"
    endpoint = "home"

    def get(self):
        restaurants = repo.get_restaurants()
        return self.render_template(
            "home.html", restaurants=restaurants, food_or_drink=FoodOrDrink
        )
