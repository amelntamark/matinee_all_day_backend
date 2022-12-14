from cProfile import run
from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.UserData import UserData


users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


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


@users_bp.route("/login",  methods=["POST"])
def login():
    """Searches for a user by username, if not found creates new user, and returns user_id"""
    request_body = request.get_json()
    username = request_body['username']

    user = UserData.query.filter_by(username=username).first()
    if user is None:
        user = UserData(
            username=request_body['username'])
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": f"User created",
            "username": f"{user.username}",
            "id": user.user_id
        }), 201

    return jsonify({
        "message": f"You are now logged in.",
        "username": f"{user.username}",
        "id": user.user_id
    }), 200
