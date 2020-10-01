from app.utils import search_location
from flask import abort
from flask import jsonify
from flask import request
from flask.views import MethodView


# from app.models import tags_


class LocationAPI(MethodView):
    rule = "/api/location"
    endpoint = "location"

    def get(self):
        q = request.args.get("q")
        return jsonify(search_location(q)) if q else abort(400)


# class TagAPI(MethodView):
#     rule = "/api/tag"
#     endpoint = "tag"
#
#     def get(self):
#         return jsonify([i.name for i in tags_])


# @admin.route("/tags")
# def tags():
#     return
