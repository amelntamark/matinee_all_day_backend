import os
import requests
import random
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, make_response, abort


TMDB_PATH = "https://api.themoviedb.org/3/discover/movie"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")


def get_horror_movie():
    QUERY_PARAMS = {
        "api_key": TMDB_API_KEY,
        "with_genres": "27",
        "sort_by": "vote_average.desc",
        "vote_count.gte": "364"
    }

    response = requests.get(TMDB_PATH, params=QUERY_PARAMS)
    response = response.json()

    movie_titles = []

    for movie in response["results"]:
        movie_titles.append(movie["title"])

    random_number = random.randint(0, len(movie_titles)-1)
    print(movie_titles[random_number])


get_horror_movie()
