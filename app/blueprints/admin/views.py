from app import repo
from app.models.db import Restaurant
from app.models.forms import FindRestaurantForm
from app.models.forms import RestaurantReviewForm
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.views import MethodView
from flask_login import login_required


class AdminDashboardView(MethodView):
    rule = "/dashboard"
    endpoint = "dashboard"

    decorators = (login_required,)

    def get(self):
        return render_template("dashboard.html")


class FindRestaurantView(MethodView):
    rule = "/find-restaurant"
    endpoint = "find_restaurant"

    decorators = (login_required,)

    def get(self):
        form = FindRestaurantForm()
        return render_template("find_restaurant.html", form=form)


class CreateReviewView(MethodView):
    rule = "/create-review"
    endpoint = "create_review"

    decorators = (login_required,)

    def get(self):
        form = RestaurantReviewForm()
        return render_template("create_review.html", form=form)

    def post(self):
        form = RestaurantReviewForm(request.form)
        if form.validate_on_submit():
            restaurant = Restaurant.from_form(form)
            repo.save_restaurant(restaurant)
            return redirect(url_for("blog.home"))
        else:
            return render_template("create_review.html", form=form)
