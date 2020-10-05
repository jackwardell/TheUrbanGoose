from .admin import admin as admin_group
from .auth import auth as auth_group
from .blog import blog as blog_group

__all__ = ["blog_group", "admin_group", "auth_group"]
