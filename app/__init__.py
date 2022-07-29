from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from app.models.user import User
    from app.models.session import Session

    # Register Blueprints here
    from .sessions_routes import sessions_bp
    app.register_blueprint(sessions_bp)

    # from .horror_route import horror_bp  # This BP is a test
    # app.register_blueprint(horror_bp)

    return app
