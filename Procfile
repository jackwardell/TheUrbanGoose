release: python cli.py db upgrade
web: gunicorn -w 1 -b 0.0.0.0:$PORT "app:create_app()"
