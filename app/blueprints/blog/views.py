from app import repo
from app.flask_simpleview import View


class HomeView(View):
    rule = "/"
    endpoint = "home"

    def get(self):
        restaurants = repo.get_all_restaurants()
        return self.render_template("home.html", restaurants=restaurants)
