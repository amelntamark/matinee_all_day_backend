from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.UserData import UserData


users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@users_bp.route("", methods=["POST"])
def create_user():
    """Adds new user to user database."""
    request_body = request.get_json()
    new_user = UserData(
        user_name=request_body['user_name'], seen_it='')

    request_body = request.get_json()
    new_user = UserData(
        user_name=request_body['user_name'])

    db.session.add(new_user)
    db.session.commit()

    return f"User {new_user.user_name} created successfully :)"

    return f"User account for  {new_user.user_name} created."


@users_bp.route("/<user_id>/<movie_id>", methods=["PATCH"])
def add_to_users_seen_list(user_id, movie_id):
    """Adds a movie's TMdB ID to a users seen list"""

    # TODO: Get user's seen list. Append a new movie to it. Return it.
    user = UserData.query.get(user_id)
    seen_list = user.seen_it

    if seen_list != None:  # User's seen it list is not empty
        user.seen_it = user.seen_it + ", " + movie_id
    else:  # User's seen it list is empty
        user.seen_it = movie_id

    db.session.commit()

    return f"{user.username}'s seen list: {user.seen_it}."
