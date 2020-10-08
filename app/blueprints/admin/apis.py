from app.flask_simpleview import API
from app.utils import search_location
from flask import abort
from flask import request
from flask_login import login_required


class LocationAPI(API):
    rule = "/api/location"
    endpoint = "location"

    decorators = (login_required,)

    def get(self):
        q = request.args.get("q")
        return self.jsonify(search_location(q)) if q else abort(400)
