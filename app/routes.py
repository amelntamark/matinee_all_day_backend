import os
import requests
import random
from dotenv import load_dotenv
from flask import Flask, Blueprint, request, jsonify, make_response, abort

load_dotenv()

TMDB_PATH = "https://api.themoviedb.org/3/discover/movie"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

genres_bp = Blueprint("genres_bp", __name__, url_prefix="/genres")


@genres_bp.route("", methods=["POST"])
def post_genre_preferences():
    """Posts genre preferences from user to the MAD API.
    Requests should be in JSON format per this example: {"genres": ["horror", "thriller", "drama"]}"""

    # Validate data in request body. If valid, add to session database.
