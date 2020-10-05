from functools import wraps

from app import repo
from app.blueprints.auth.forms import LoginForm
from app.flask_simpleview import View
from flask import current_app
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user


def is_safe_url(path):
    return path in [i.rule for i in current_app.url_map.iter_rules()]


def redirect_if_logged_in(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("admin.dashboard"))
        else:
            return func(*args, **kwargs)

    return decorated_function


class LoginView(View):
    rule = "/login"
    endpoint = "login"

    decorators = (redirect_if_logged_in,)

    def get(self):
        form = LoginForm()
        return self.render_template("login.html", form=form)

    def post(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = repo.get_user(form.username.data)
            login_user(user)

            next_page = request.args.get("next")
            if next_page and is_safe_url(next_page):
                return self.redirect(next_page)
            else:
                return self.redirect(url_for("admin.dashboard"))

        else:
            return self.render_template("login.html", form=form)


class LogoutView(View):
    rule = "/logout"
    endpoint = "logout"

    decorators = (login_required,)

    def get(self):
        logout_user()
        return self.redirect(url_for("blog.home"))
