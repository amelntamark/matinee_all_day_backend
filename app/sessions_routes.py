from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.session import Session
from app.models.UserData import UserData
import os
import requests
import random
from alembic import op


sessions_bp = Blueprint('sessions_bp', __name__, url_prefix='/sessions')

TMDB_PATH = "https://api.themoviedb.org/3/discover/movie"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

# Gerne options on front end will be limited to these
TMDB_GENRES = {"Action": "28",
               "Adventure": "12",
               "Animation": "16",
               "Comedy": "35",
               "Crime": "80",
               "Documentary": "99",
               "Drama": "18",
               "Family": "10751",
               "Fantasy": "14",
               "History": "36",
               "Horror": "27",
               "Music": "10402",
               "Mystery": "9648",
               "Romance": "10749",
               "SciFi": "878",
               #    "TV Movie": "10770",
               "Thriller": "53",
               "War": "10752",
               "Western": "37"}


TMDB_DECADES = {"1970s": ["1970-01-01T00:00:00.000Z", "1979-12-31T00:00:00.000Z"],
                "1980s": ["1980-01-01T00:00:00.000Z", "1989-12-31T00:00:00.000Z"],
                "1990s": ["1990-01-01T00:00:00.000Z", "1999-12-31T00:00:00.000Z"],
                "2000s": ["2000-01-01T00:00:00.000Z", "2009-12-31T00:00:00.000Z"],
                "2010s": ["2000-01-01T00:00:00.000Z", "2009-12-31T00:00:00.000Z"],
                "2020 onward": ["2020-01-01T00:00:00.000Z", ""]}

TMDB_RUNTIMES = {"90 minutes": "96",
                 "2 hours": "126"}

# change user preferences to TMDB speak


def translate_to_TMDB_params(session):
    tmdb_params = {
        "api_key": TMDB_API_KEY,
        "include_adult": False,
        "with_original_language": "en",
        "page": 1,
        "sort_by": "vote_average.desc",
        "vote_count.gte": "364"}
    if session.era:
        tmdb_params["primary_release_date.gte"] = TMDB_DECADES[session.era][0]
        tmdb_params["primary_release_date.lte"] = TMDB_DECADES[session.era][1]
    if session.genre:
        genre_preference_list = list(session.genre.split(" "))
        tmdb_genre_list = []
        for pref in genre_preference_list:
            tmdb_genre_list.append(TMDB_GENRES[pref])
        tmdb_genres_str = ",".join(tmdb_genre_list)
        tmdb_params["with_genres"] = tmdb_genres_str
    if session.runtime:
        tmdb_params["with_runtime.lte"] = TMDB_RUNTIMES[session.runtime]
    print(tmdb_params)
    return tmdb_params


# POST a session
@ sessions_bp.route("", methods=['POST'])
def create_session():
    request_body = request.get_json()
    new_session = Session(
        genre=request_body['genre'], era=request_body['era'], runtime=request_body['runtime'], user_id=request_body['user_id'])

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
    random_num = random.randint(0, len(response["results"])-1)

    return response["results"][random_num], 200

# May want to have a column in sessions table called user_id. If user is not logged in, value is null. Else, it's an int.
