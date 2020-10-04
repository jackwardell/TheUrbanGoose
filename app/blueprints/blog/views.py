from app import repo
from flask import render_template
from flask.views import MethodView


class HomeView(MethodView):
    rule = "/"
    endpoint = "home"

    def get(self):
        restaurants = repo.get_all_restaurants()
        return render_template("home.html", restaurants=restaurants)
