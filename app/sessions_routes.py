from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.session import Session
from app.models.UserData import UserData
import os
import requests
import random
from app.movie_finder import *


sessions_bp = Blueprint('sessions_bp', __name__, url_prefix='/sessions')

TMDB_PATH = "https://api.themoviedb.org/3/discover/movie"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")


# POST a session
@ sessions_bp.route("", methods=['POST'])
def create_session():
    """Creates a new session. Takes a request with a genre, era, runtime, and user_id."""
    request_body = request.get_json()
    new_session = Session(
        genre=request_body['genre'], era=request_body['era'], runtime=request_body['runtime'], user_id=request_body['user_id'])

    db.session.add(new_session)
    db.session.commit()

    return f"Preferences saved session_id = {new_session}. "


# DELETE a session
@ sessions_bp.route('/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Deletes a session from the database."""
    session = Session.query.get(session_id)

    db.session.delete(session)
    db.session.commit()

    return f"Session {session.session_id} deleted.  The fun has ended"

# GET a movie


@ sessions_bp.route('/<session_id>', methods=['GET'])
def get_movie(session_id):
    """
    Returns a movie in JSON form based on preferences recorded during session. 
    If user is logged in, it will make sure user has not seen the movie already.
    """
    session = Session.query.get(session_id)
    response = call_tmdb(session_id)
    random_movie = get_random_movie(response)

    # If user is logged in:
    if session.user_id:
        user = UserData.query.get(session.user_id)
        while str(random_movie["id"]) in user.seen_it:
            random_movie = get_random_movie(response)

    return random_movie, 200
