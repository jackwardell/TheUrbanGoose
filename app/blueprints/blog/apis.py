from app import repo
from app.flask_simpleview import API
from flask import request


class RestaurantAPI(API):
    rule = "/api/restaurants"
    endpoint = "restaurants"

    def get(self):
        restaurant_id = request.args.get("id")
        if restaurant_id is None:
            restaurants = repo.get_all_restaurants()
            return self.jsonify(
                [restaurant.to_dict() for restaurant in restaurants]
            )
        else:
            restaurant = repo.get_restaurant(id=restaurant_id)
            if restaurant is None:
                return self.jsonify({"status": "no restaurant found"})
            else:
                return self.jsonify(restaurant.to_dict())
