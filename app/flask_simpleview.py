import flask
from flask import Blueprint
from flask.views import MethodView


class Group(Blueprint):
    def add_view(self, view):
        self.add_url_rule(view.rule, view_func=view.as_view(view.endpoint))

    def add_api(self, api):
        self.add_view(api)


class View(MethodView):
    @property
    def rule(self):
        raise NotImplementedError()

    @property
    def endpoint(self):
        raise NotImplementedError()

    def __getattr__(self, item):
        return getattr(flask, item)


API = View
