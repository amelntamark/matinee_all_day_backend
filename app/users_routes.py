from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
<<<<<<< HEAD
from app.models.user import UserData
=======
from app.models.user_data import UserData
>>>>>>> 0b68fd760bc041cfbfed34bb17d43003847bcdb4


users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@users_bp.route("", methods=["POST"])
def create_user():
    """Adds new user to user database."""
    request_body = request.get_json()
    new_user = UserData(
        user_name=request_body['user_name'], seen_it='')

<<<<<<< HEAD
    db.session.add(new_user)
    db.session.commit()
    # TODO: Figure out shape of request and add user to database with unique primary key.
    # Will probably also need to verify that user/username does not already exist.
=======
    request_body = request.get_json()
    new_user = UserData(
        username=request_body['username'])

    db.session.add(new_user)
    db.session.commit()

    return f"User {new_user.username} created successfully :)"
>>>>>>> 0b68fd760bc041cfbfed34bb17d43003847bcdb4

    return f"User account for  {new_user.user_name} created."


@users_bp.route("/<user_id>/<movie_id>", methods=["PATCH"])
def add_to_users_seen_list(user_id, movie_id):
    """Adds a movie's TMdB ID to a users seen list"""

    # TODO: validate data and add the TMdB ID of a movie to the seen column in the user database.
