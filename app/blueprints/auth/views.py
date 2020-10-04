from app import repo
from app.blueprints.auth.forms import LoginForm
from app.flask_simpleview import View
from flask import request
from flask import url_for
from flask_login import login_user
from flask_login import logout_user


class LoginView(View):
    rule = "/login"
    endpoint = "login"

    def get(self):
        form = LoginForm()
        return self.render_template("login.html", form=form)

    def post(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = repo.get_user(form.username.data)
            login_user(user)
            return self.redirect(url_for("admin.dashboard"))

        else:
            return self.render_template("login.html", form=form)


class LogoutView(View):
    rule = "/logout"
    endpoint = "logout"

    def get(self):
        logout_user()
        return self.redirect(url_for("blog.home"))
