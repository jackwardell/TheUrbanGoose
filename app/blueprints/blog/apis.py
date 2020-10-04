from app import repo
from flask import jsonify
from flask import request
from flask.views import MethodView


# class LocationsAPI(MethodView):
#     rule = "/api/locations"
#     endpoint = "locations"
#
#     def get(self):
#         reviews = repo.get_all_restaurants()
#         return jsonify([review.to_dict() for review in reviews])


class RestaurantAPI(MethodView):
    rule = "/api/restaurants"
    endpoint = "restaurants"

    def get(self):
        restaurant_id = request.args.get("id")
        if restaurant_id is None:
            restaurants = repo.get_all_restaurants()
            return jsonify(
                [restaurant.to_dict() for restaurant in restaurants]
            )
        else:
            restaurant = repo.get_restaurant(id=restaurant_id)
            if restaurant is None:
                return jsonify({"status": "no restaurant found"})
            else:
                return jsonify(restaurant.to_dict())
