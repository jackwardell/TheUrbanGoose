from flask import Flask
from settings import SECRET_KEY
from settings import SQLALCHEMY_URL


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_URL
    assert (
        SQLALCHEMY_DATABASE_URI
    ), "Enter a SQLALCHEMY_URL environment variable"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "development"
    DEBUG = False
    TESTING = False
    SECRET_KEY = SECRET_KEY
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # try:
    #     SECRET_KEY = os.getenv('SECRET_KEY').encode('utf-8')
    # except AttributeError:
    #     raise KeyError('Enter a secret key!')

    def __repr__(self):
        return self.__class__.__name__


class TestingConfig(BaseConfig):
    ENV = "production"
    TESTING = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False


def configure_app(app: Flask):
    """
    Configure the flask app to the appropriate environment
    :param app: Our flask application
    """
    # assert os.getenv('GOOSE_ENV') in ('development', 'testing', 'production'), \
    #     "WEBAPP_ENV must be either development, testing or production"

    config = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }["development"]
    app.config.from_object(config)
