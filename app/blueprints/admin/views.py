from functools import wraps

from app import repo
from app.blueprints.admin.forms import CreateRestaurantReviewForm
from app.blueprints.admin.forms import FindRestaurantForm
from app.blueprints.admin.forms import UpdateOrDeleteRestaurantReviewForm
from app.flask_simpleview import View
from app.models import Restaurant
from app.utils import get_food_and_or_drink
from flask import abort
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import url_for
from flask_login import login_required


def get_restaurant(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        restaurant_id = request.args.get("id") or abort(404)
        restaurant = repo.get_restaurant(restaurant_id) or abort(404)
        g.restaurant = restaurant
        return func(*args, **kwargs)

    return decorator


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
        form = CreateRestaurantReviewForm()
        return self.render_template("create_restaurant_review.html", form=form)

    def post(self):
        form = CreateRestaurantReviewForm(request.form)
        if form.validate_on_submit():
            restaurant = Restaurant.from_form(form)
            # slack.chat.post_message('created-restaurants', text=restaurant.query_string())
            repo.save_restaurant(restaurant)
            return redirect(url_for("blog.home"))
        else:
            return self.render_template(
                "create_restaurant_review.html", form=form
            )


class RestaurantReviewsView(View):
    rule = "/restaurant-reviews"
    endpoint = "restaurant_reviews"

    decorators = (login_required,)

    def get(self):
        restaurants = repo.get_restaurants(archived=True)
        return self.render_template(
            "restaurant_reviews.html", restaurants=restaurants
        )


class RestaurantReviewView(View):
    rule = "/restaurant-review"
    endpoint = "restaurant_review"
    template = "restaurant_review.html"

    decorators = (login_required, get_restaurant)

    def get(self):
        params = (
            g.restaurant.to_dict() if hasattr(g, "restaurant") else abort(404)
        )
        params["food_or_drink"] = get_food_and_or_drink(
            for_drink=params["for_drink"], for_food=params["for_food"]
        )
        # import IPython; IPython.embed()
        params["tags"] = [tag.name for tag in g.restaurant.tags]
        form = UpdateOrDeleteRestaurantReviewForm(**params)
        return self.render_template(form=form)

    def post(self):
        form = UpdateOrDeleteRestaurantReviewForm(request.form)
        # todo: assert not 2 fields are posted
        if form.archive.data is True:
            repo.archive_restaurant(g.restaurant)
            flash(
                f'Successfully Archived: <a href="{url_for("admin.restaurant_review", id=g.restaurant.id)}">{g.restaurant.name}</a>',
                category="success",
            )
            return redirect(url_for("admin.restaurant_reviews"))
        elif form.unarchive.data is True:
            repo.unarchive_restaurant(g.restaurant)
            flash(
                f'Successfully Unarchived: <a href="{url_for("admin.restaurant_review", id=g.restaurant.id)}">{g.restaurant.name}</a>',
                category="success",
            )
            return redirect(url_for("admin.restaurant_reviews"))
        elif form.delete.data is True:
            repo.delete_restaurant(g.restaurant)
            flash(
                f"Successfully Deleted: {g.restaurant.name}",
                category="success",
            )
            return redirect(url_for("admin.restaurant_reviews"))
        elif form.update.data is True and form.validate_on_submit():
            restaurant = Restaurant.from_form(form)
            repo.update_restaurant(restaurant)
            flash(
                f'Successfully Updated: <a href="{url_for("admin.restaurant_review", id=restaurant.id)}">{restaurant.name}</a>',
                category="success",
            )
            return redirect(url_for("admin.restaurant_reviews"))
        else:
            return self.render_template(form=form)
