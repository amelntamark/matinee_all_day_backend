import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    # Register Blueprints here
    from .horror_route import horror_bp
    app.register_blueprint(horror_bp)

    return app
