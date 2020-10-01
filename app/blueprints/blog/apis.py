from app import repo
from flask import jsonify
from flask.views import MethodView


class LocationsAPI(MethodView):
    rule = "locations"
    endpoint = "locations"

    def get(self):
        reviews = repo.get_all_reviews()
        return jsonify([review.to_dict() for review in reviews])
