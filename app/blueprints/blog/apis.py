from app import repo
from app.flask_simpleview import API
from app.static import FoodOrDrink
from flask import request


class RestaurantAPI(API):
    rule = "/api/restaurants"
    endpoint = "restaurants"

    def get(self):
        restaurant_id = request.args.get("id")
        food_or_drink = request.args.get("food_or_drink", FoodOrDrink.EITHER)
        if restaurant_id is None:
            restaurants = repo.get_restaurants(food_or_drink=food_or_drink)
            return self.jsonify(
                [restaurant.to_dict() for restaurant in restaurants]
            )
        else:
            restaurant = repo.get_restaurant(id=restaurant_id)
            if restaurant is None:
                return self.jsonify({"status": "no restaurant found"})
            else:
                return self.jsonify(restaurant.to_dict())
