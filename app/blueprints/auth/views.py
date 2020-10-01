from app.models.forms import LoginForm
from flask import render_template
from flask import request
from flask.views import MethodView


class LoginView(MethodView):
    rule = "/login"
    endpoint = "login"

    def get(self):
        form = LoginForm()
        return render_template("login.html", form=form)

    def post(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            pass
        else:
            return render_template("login.html", form=form)
