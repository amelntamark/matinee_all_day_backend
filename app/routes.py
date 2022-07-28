import os
import requests
import random
from dotenv import load_dotenv
from flask import Flask, Blueprint, request, jsonify, make_response, abort

load_dotenv()

TMDB_PATH = "https://api.themoviedb.org/3/discover/movie"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

genres_bp = Blueprint("genres_bp", __name__, url_prefix="/genres")
eras_bp = Blueprint("eras_bp", __name__, url_prefix="/eras")
runtime_bp = Blueprint("runtime_bp", __name__, url_prefix="/runtime")
end_session_bp = Blueprint("end_session_bp", __name__,
                           url_prefix="/end_session")
create_user_bp = Blueprint("create_user_bp", __name__,
                           url_prefix="/create_user")


@genres_bp.route("", methods=["POST"])
def post_genre_preferences():
    """Posts genre preferences from user to the MAD API.
    Requests should be in JSON format per this example: {"genres": ["horror", "thriller", "drama"]}"""

    # TODO: Validate data in request body. If valid, add to session database.

    # Basic tester implementation
    request_body = request.get_json()
    response_string = f"Recorded your preference for: {request_body['genres']}"

    return response_string


@eras_bp.route("", methods=["POST"])
def post_era_preferences():
    """Posts preferences for release dates (by decades) to MAD API.
    Request should be in JSON format: {"eras": ["1980s", "1990s", "2000s", "2010s", "2020s"]}"""

    # TODO: Validate data and add to session database.

    # Basic tester implementation
    request_body = request.get_json()
    response_string = f"Recorded your preference for: {request_body['eras']}"

    return response_string


@runtime_bp.route("", methods=["POST"])
def post_runtime_preferences():
    """Posts user's runtime preferences to MAD API.
    Request should be in JSON format: {"runtime": "< 120 mins"}"""

    # TODO: Validate data and add to session database.

    # Basic tester implementation
    request_body = request.get_json()
    response_string = f"Recorded your preference for: {request_body['runtime']}"

    return response_string


@end_session_bp.route("/<session_id>", methods=["DELETE"])
def end_current_session(session_id):
    """Ends current session by deleting temporary information from the sessions database"""

    # TODO: Remove data from the database


@create_user_bp.route("", methods=["POST"])
def create_user():
    """Adds new user to user database."""

    # TODO: Figure out shape of request and add user to database with unique primary key.
    # Will probably also need to verify that user/username does not already exist.
