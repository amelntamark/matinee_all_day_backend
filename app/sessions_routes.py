from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.session import Session
import os
import requests


sessions_bp = Blueprint('sessions_bp', __name__, url_prefix='/sessions')

TMDB_PATH = "https://api.themoviedb.org/3/discover/movie"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

# Gerne options on front end will be limited to these
TMDB_GENRES = {"Action": 28,
               "Adventure": 12,
               "Animation": 16,
               "Comedy": 35,
               "Crime": 80,
               "Documentary": 99,
               "Drama": 18,
               "Family": 10751,
               "Fantasy": 14,
               "History": 36,
               "Horror": 27,
               "Music": 10402,
               "Mystery": 9648,
               "Romance": 10749,
               "Science Fiction": 878,
               "TV Movie": 10770,
               "Thriller": 53,
               "War": 10752,
               "Western": 37}


TMDB_decades = {"1970s": "primary_release_date.gte : 1970-01-01T00:00:00.000Z, primary_release_date.lte: 1979-12-31T00:00:00.000Z",
                "1980s": "primary_release_date.gte : 1980-01-01T00:00:00.000Z, primary_release_date.lte: 1989-12-31T00:00:00.000Z",
                "1990s": "primary_release_date.gte : 1990-01-01T00:00:00.000Z, primary_release_date.lte: 1999-12-31T00:00:00.000Z",
                "2000s": "primary_release_date.gte : 2000-01-01T00:00:00.000Z, primary_release_date.lte: 2009-12-31T00:00:00.000Z",
                "2010s": "primary_release_date.gte : 2000-01-01T00:00:00.000Z, primary_release_date.lte: 2009-12-31T00:00:00.000Z",
                "2020 onward": "primary_release_date.gte : 2020-01-01T00:00:00.000Z"}

# change user preferences to TMDB speak


def translate_to_TMDB_params(session):
    genre_prefernce_list = list(session.genre.split(" "))
    for pref in genre_prefernce_list:
        pref = TMDB_GENRES[pref]
    tmdb_genres_str = " ".join(genre_prefernce_list)
    tmdb_params = {
        "api_key": TMDB_API_KEY,
        "include_adult": False,
        "language": "en-US",
        "page": 1,
        "with_genres": tmdb_genres_str,
        "sort_by": "vote_average.desc",
        "vote_count.gte": "364"}
    return tmdb_params


# POST a session
@ sessions_bp.route("", methods=['POST'])
def create_session():
    request_body = request.get_json()
    new_session = Session(
        genre=request_body['genre'], era=request_body['era'], runtime=request_body['runtime'])

    db.session.add(new_session)
    db.session.commit()

    return f"Preferences saved session_id = {new_session}. "

# DELETE a session


@ sessions_bp.route('/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Session.query.get(session_id)

    db.session.delete(session)
    db.session.commit()

    return f"Session {session.session_id} deleted.  The fun has ended"


@ sessions_bp.route('/<session_id>', methods=['GET'])
def get_movie(session_id):
    session = Session.query.get(session_id)
    tmdb_params = translate_to_TMDB_params(session)
    response = requests.get(TMDB_PATH, params=tmdb_params)
    response = response.json()

    return response
    # Now call the helper funciton to prepare query params
    # query_params =translate_to_TMDB_discover_params(session)
    # response = requests.get(TMDB_PATH, params=tmdb_params)
