from app import repo
from flask import render_template
from flask.views import MethodView


class HomeView(MethodView):
    rule = "/"
    endpoint = "home"

    def get(self):
        reviews = repo.get_all_reviews()
        return render_template("home.html", reviews=reviews)
