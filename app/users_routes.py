from cProfile import run
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
        username=request_body['username'])

    db.session.add(new_user)
    db.session.commit()

    return f"User {new_user.username} created successfully :)"


@users_bp.route("/<user_id>/<movie_id>", methods=["PATCH"])
def add_to_users_seen_list(user_id, movie_id):
    """Adds a movie's TMdB ID to a users seen list"""

    user = UserData.query.get(user_id)
    seen_list = user.seen_it

    if seen_list != None:  # User's seen it list is not empty
        user.seen_it = user.seen_it + ", " + movie_id
    else:  # User's seen it list is empty
        user.seen_it = movie_id

    db.session.commit()

    return f"{user.username}'s seen list: {user.seen_it}."


# @users_bp.route("/<username>", methods=["GET"])
# def check_user_login(username):
#     try:
#         user = UserData.query.get(username)
#         return user.user_id
#     except:
#         return f"Username not found"
