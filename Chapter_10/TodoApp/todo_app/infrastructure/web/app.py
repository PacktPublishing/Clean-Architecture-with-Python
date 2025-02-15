"""
Flask web application setup for the Todo App.
"""

from flask import Flask
from todo_app.infrastructure.configuration.container import Application


def create_web_app(app_container: Application) -> Flask:
    """Create and configure Flask application."""
    flask_app = Flask(__name__)
    flask_app.config["SECRET_KEY"] = "dev"  # Change this in production
    flask_app.config["APP_CONTAINER"] = app_container  # Store container in config

    # Register blueprints
    from . import routes

    flask_app.register_blueprint(routes.bp)

    return flask_app
