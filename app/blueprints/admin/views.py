from app import repo
from app.blueprints.admin.forms import FindRestaurantForm
from app.blueprints.admin.forms import RestaurantReviewForm
from app.flask_simpleview import View
from app.models import Restaurant
from flask import redirect
from flask import request
from flask import url_for
from flask_login import login_required


class AdminDashboardView(View):
    rule = "/dashboard"
    endpoint = "dashboard"

    decorators = (login_required,)

    def get(self):
        return self.render_template("dashboard.html")


class FindRestaurantView(View):
    rule = "/find-restaurant"
    endpoint = "find_restaurant"

    decorators = (login_required,)

    def get(self):
        form = FindRestaurantForm()
        return self.render_template("find_restaurant.html", form=form)


class CreateRestaurantReviewView(View):
    rule = "/create-restaurant-review"
    endpoint = "create_restaurant_review"

    decorators = (login_required,)

    def get(self):
        form = RestaurantReviewForm()
        return self.render_template("create_restaurant_review.html", form=form)

    def post(self):
        form = RestaurantReviewForm(request.form)
        if form.validate_on_submit():
            restaurant = Restaurant.from_form(form)
            repo.save_restaurant(restaurant)
            return redirect(url_for("blog.home"))
        else:
            return self.render_template(
                "create_restaurant_review.html", form=form
            )


# class EditReviewView(View):
#     rule = "/edit-review"
#     endpoint = "edit-review"
#
#     decorators = (login_required,)
#
#     def get(self):
#         restaurant_id = request.args.get("id")
#         repo.get_restaurant()
#         form = RestaurantReviewForm(**)
