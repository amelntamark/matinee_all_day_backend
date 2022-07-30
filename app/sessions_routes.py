from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.session import Session
import os
import requests


sessions_bp = Blueprint('sessions_bp', __name__, url_prefix='/sessions')

TMDB_PATH = "https://api.themoviedb.org/3/discover/movie"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")


def translate_to_TMDB_params(session):
    pass
    # POST a session


@sessions_bp.route("", methods=['POST'])
def create_session():
    request_body = request.get_json()
    new_session = Session(
        genre=request_body['genre'], era=request_body['era'], runtime=request_body['runtime'])

    db.session.add(new_session)
    db.session.commit()

    return f"Preferences saved session_id = {new_session.session_id}. Ready to search"

# DELETE a session


@sessions_bp.route('/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Session.query.get(session_id)

    db.session.delete(session)
    db.session.commit()

    return f"Session {session.session_id} deleted.  The fun has ended"


@sessions_bp.route('/<session_id>', methods=['GET'])
def get_movie(session_id):
    session = Session.query.get(session_id)
    # Now call the helper funciton to prepare query params
    # query_params =translate_to_TMDB_discover_params(session)
    # response = requests.get(TMDB_PATH, params=query_params)

    #     QUERY_PARAMS = {
#         "api_key": TMDB_API_KEY,
#         "with_genres": "27",
#         "sort_by": "vote_average.desc",
#         "vote_count.gte": "364"
