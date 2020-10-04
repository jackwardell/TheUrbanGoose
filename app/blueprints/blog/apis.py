from app import repo
from flask import jsonify
from flask import request
from flask.views import MethodView


class LocationsAPI(MethodView):
    rule = "/api/locations"
    endpoint = "locations"

    def get(self):
        reviews = repo.get_all_restaurants()
        return jsonify([review.to_dict() for review in reviews])


class RestaurantAPI(MethodView):
    rule = "/api/restaurant"
    endpoint = "restaurant"

    def get(self):
        restaurant_id = request.args.get("id")
        if restaurant_id is None:
            return jsonify({"status": "no restaurant"})
        else:
            review = repo.get_restaurant(id=restaurant_id)
            if review is None:
                return jsonify({"status": "no restaurant found"})
            else:
                return jsonify(review.to_dict())
