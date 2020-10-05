from contextlib import contextmanager

import click
from app import create_app
from flask.cli import FlaskGroup
from settings import DB_NAME
from settings import DB_USER
from settings import LOCAL_DB_URL
from settings import SQLALCHEMY_URL
from sqlalchemy import create_engine

flask_cli = FlaskGroup(create_app=create_app)


@contextmanager
def engine_scope(url=SQLALCHEMY_URL):
    engine = create_engine(url)
    yield engine
    engine.dispose()


@contextmanager
def connection_scope(url=SQLALCHEMY_URL):
    with engine_scope(url) as engine:
        conn = engine.connect()
        conn.execute("commit")
        yield conn
        conn.execute("commit")
        conn.close()


@contextmanager
def execute_scope(url=SQLALCHEMY_URL):
    def execute(command):
        with connection_scope(url=url) as conn:
            return conn.execute(command)

    yield lambda command: execute(command)


def _setup_db() -> None:
    with execute_scope(url=LOCAL_DB_URL) as execute:
        execute(f"CREATE DATABASE {DB_NAME}")
        execute(f"CREATE USER {DB_USER}")
        execute(f"ALTER ROLE {DB_USER} SUPERUSER")
        execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")


def _drop_db() -> None:
    with execute_scope(url=LOCAL_DB_URL) as execute:
        print(LOCAL_DB_URL)
        _kill_connections()
        execute(f"DROP DATABASE {DB_NAME}")
        execute(f"DROP USER {DB_USER}")


def _kill_connections() -> None:
    with execute_scope(url=LOCAL_DB_URL) as execute:
        execute(
            f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
            f"FROM pg_stat_activity "
            f"WHERE pid <> pg_backend_pid()"
            f"AND datname = '{DB_NAME}';"
        )


@click.group()
def db():
    pass


@db.command()
def setup():
    """Set up database"""
    return _setup_db()


@db.command()
def drop():
    """Tear down database"""
    return _drop_db()


cli = click.CommandCollection(sources=[flask_cli, db])

if __name__ == "__main__":
    cli()
