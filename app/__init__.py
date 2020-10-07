from app.config import configure_app
from app.event_system import EventSystem
from app.models import Anon
from app.models import db
from app.models import PageView
from app.models import Repository
from app.utils import request_to_record
from flask import Flask
from flask import request
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from slack_time import get_slack_time

login_manager = LoginManager()
toolbar = DebugToolbarExtension()
migrate = Migrate()

event_system = EventSystem()
repo = Repository()

slack = get_slack_time()


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
    login_manager.anonymous_user = Anon

    from app import blueprints

    app.register_blueprint(blueprints.blog_group)
    app.register_blueprint(blueprints.admin_group)
    app.register_blueprint(blueprints.auth_group)

    @login_manager.user_loader
    def load_user(username):
        return repo.get_user(username)

    @app.after_request
    def after_request(response):
        if request_to_record(request):
            page_view = PageView.from_response(response)
            # todo uncomment when needed
            # repo.record_page_view(page_view)
            slack.chat.post_message("page-views", str(page_view))
        return response

    return app
