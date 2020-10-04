import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv(dotenv_path=Path(".") / ".env")


def get_env(env_name):
    if env_name not in os.environ:
        raise EnvironmentError(f"No environment variable {env_name}")
    else:
        return os.getenv(env_name)


def make_sqlalchemy_url():
    url = get_env("SQLALCHEMY_URL")
    engine = create_engine(url)
    try:
        engine.connect()
        engine.dispose()
        return url
    except OperationalError:
        return "postgresql://localhost/"


SQLALCHEMY_URL = make_sqlalchemy_url()
SLACK_API_TOKEN = get_env("SLACK_API_TOKEN")

SECRET_KEY = get_env("SECRET_KEY")

USERNAME = get_env("USERNAME")
PASSWORD = get_env("PASSWORD")

LOCAL_DB_URL = "postgresql://localhost/"

DB_NAME = "goose"
DB_USER = "goose"

ENVIRONMENT = get_env("GOOSE_ENV")

engine = create_engine(SQLALCHEMY_URL)
