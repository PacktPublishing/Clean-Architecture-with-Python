# order_system/web/app.py
import os
from flask import Flask, render_template
from ..config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register routes
    from . import legacy_routes, clean_routes

    app.register_blueprint(legacy_routes.bp)
    app.register_blueprint(clean_routes.bp)

    @app.route("/")
    def index():
        return render_template(
            "index.html", use_clean=app.config.get("USE_CLEAN_ARCHITECTURE", True)
        )

    return app
