from app.config import configure_app
from app.event_system import EventSystem
from app.models import db
from app.models import Repository
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate

login_manager = LoginManager()
toolbar = DebugToolbarExtension()
migrate = Migrate()

event_system = EventSystem()
repo = Repository()


def create_app():
    app = Flask(__name__)
    configure_app(app)

    db.init_app(app)
    toolbar.init_app(app)
    login_manager.init_app(app)
    event_system.init_app(app)
    migrate.init_app(app, db)
    repo.init_db(db.session)

    login_manager.login_view = "auth.login"

    from app import blueprints

    app.register_blueprint(blueprints.blog)
    app.register_blueprint(blueprints.admin)
    app.register_blueprint(blueprints.auth)

    @login_manager.user_loader
    def load_user(username):
        return repo.get_user(username)

    return app
