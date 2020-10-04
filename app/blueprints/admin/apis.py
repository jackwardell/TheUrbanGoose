from app.flask_simpleview import API
from app.utils import search_location
from flask import abort
from flask import request


class LocationAPI(API):
    rule = "/api/location"
    endpoint = "location"

    def get(self):
        q = request.args.get("q")
        return self.jsonify(search_location(q)) if q else abort(400)
