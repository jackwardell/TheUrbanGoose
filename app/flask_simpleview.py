# todo make this into a pypi packaged for simple flask views
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

    def render_template(self, *optional_template, **context):
        template = optional_template[0] if optional_template else self.template
        return flask.render_template(template, **context)

    def __getattr__(self, item):
        return getattr(flask, item)


# class TemplateView(View, ABC):
#
#     @property
#     def template(self):
#         raise NotImplementedError()


API = View
