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


@genres_bp.route("", methods=["POST"])
def post_genre_preferences():
    """Posts genre preferences from user to the MAD API.
    Requests should be in JSON format per this example: {"genres": ["horror", "thriller", "drama"]}"""

    # Validate data in request body. If valid, add to session database.

    # Basic tester implementation
    request_body = request.get_json()
    response_string = f"Recorded your preference for: {request_body['genres']}"

    return response_string


@eras_bp.route("", methods=["POST"])
def post_era_preferences():
    """Posts preferences for release dates (by decades) to MAD API.
    Request should be in JSON format: {"eras": ["1980s", "1990s", "2000s", "2010s", "2020s"]}"""

    # Validate data and add to session database.


@runtime_bp.route("", methods=["POST"])
def post_runtime_preferences():
    """Posts user's runtime preferences to MAD API.
    Request should be in JSON format: {"runtime": "< 120 mins"}"""

    # Validate data and add to session database.
