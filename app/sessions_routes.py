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


# PUT recommendations for this session into database
# USE WITH CAUTION! PLEASE READ DOCSTRING
@sessions_bp.route('/<session_id>', methods=['PUT'])
def store_recommendations(session_id):
    """Calls function that gets recommendations and stores them in the database.
    This method should only be called once per session ID to avoid crowding the database and making
    too many requests to TMDB API.
    """
    # TODO: Add way to check method has not been called for session_id already. If it has, return 429.
    # Current thought is to add a column to session table called "movies_fetched" that is automatically set to false, then
    # changing this value to true when movie recs have been fetched. Then this function will check that value BEFORE calling
    # get_recommendations() and will return an error message if  recs already fetched.
    get_recommendations(session_id)

    return {"message": "success"}, 201


# GET a movie
@ sessions_bp.route('/<session_id>', methods=['GET'])
def get_movie(session_id):
    """
    Returns a movie in JSON form based on preferences recorded during session. 
    """
    session = Session.query.get(session_id)
    random_movie = get_random_movie(session_id)

    # If user is logged in:
    if session.user_id:
        user = UserData.query.get(session.user_id)
        while str(random_movie["id"]) in user.seen_it:
            random_movie = get_random_movie(session_id)

    return jsonify(random_movie), 200
