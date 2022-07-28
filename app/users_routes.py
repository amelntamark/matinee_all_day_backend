from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.user import User


users_bp = Blueprint('users_bp', __name__, url_prefix='users')


@users_bp.route("", methods=["POST"])
def create_user():
    """Adds new user to user database."""

    # TODO: Figure out shape of request and add user to database with unique primary key.
    # Will probably also need to verify that user/username does not already exist.


@users_bp.route("/<user_id>/<movie_id>", methods=["PATCH"])
def add_to_users_seen_list(user_id, movie_id):
    """Adds a movie's TMdB ID to a users seen list"""

    # TODO: validate data and add the TMdB ID of a movie to the seen column in the user database.
