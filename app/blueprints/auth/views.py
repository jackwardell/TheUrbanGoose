from app import repo
from app.models.forms import LoginForm
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.views import MethodView
from flask_login import login_user
from flask_login import logout_user


class LoginView(MethodView):
    rule = "/login"
    endpoint = "login"

    def get(self):
        form = LoginForm()
        return render_template("login.html", form=form)

    def post(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = repo.get_user(form.username.data)
            login_user(user)
            return redirect(url_for("admin.dashboard"))

        else:
            return render_template("login.html", form=form)


class LogoutView(MethodView):
    rule = "/logout"
    endpoint = "logout"

    def get(self):
        logout_user()
        return redirect(url_for("blog.home"))
