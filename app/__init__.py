import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    # Register Blueprints here
    from .routes import genres_bp, eras_bp, runtime_bp
    app.register_blueprint(genres_bp)
    app.register_blueprint(eras_bp)
    app.register_blueprint(runtime_bp)

    from .horror_route import horror_bp  # This BP is a test
    app.register_blueprint(horror_bp)

    return app
