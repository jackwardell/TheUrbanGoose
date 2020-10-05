from flask import Flask
from settings import ENVIRONMENT
from settings import SECRET_KEY
from settings import SQLALCHEMY_URL


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = SECRET_KEY
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    def __repr__(self):
        return self.__class__.__name__


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False
    DEBUG_TB_ENABLED = False


def configure_app(app: Flask):
    """
    Configure the flask app to the appropriate environment
    """
    config = {"development": DevelopmentConfig, "production": ProductionConfig}
    app.config.from_object(config[ENVIRONMENT])
