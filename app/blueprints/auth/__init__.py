from app.flask_simpleview import Group

from .views import LoginView
from .views import LogoutView

auth = Group("auth", __name__, url_prefix="/", template_folder="templates")

auth.add_view(LoginView)
auth.add_view(LogoutView)
