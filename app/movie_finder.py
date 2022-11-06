from app.models.session import Session
from app.models.Movie import Movie
from app import db
import random
import requests
import os

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
               "Thriller": "53",
               "War": "10752",
               "Western": "37"}


TMDB_DECADES = {"1970s": ["1970-01-01T00:00:00.000Z", "1979-12-31T00:00:00.000Z"],
                "1980s": ["1980-01-01T00:00:00.000Z", "1989-12-31T00:00:00.000Z"],
                "1990s": ["1990-01-01T00:00:00.000Z", "1999-12-31T00:00:00.000Z"],
                "2000s": ["2000-01-01T00:00:00.000Z", "2009-12-31T00:00:00.000Z"],
                "2010s": ["2010-01-01T00:00:00.000Z", "2019-12-31T00:00:00.000Z"],
                "2020 Onward": ["2020-01-01T00:00:00.000Z", "2022-06-01T00:00:00.000Z"]}

TMDB_RUNTIMES = {"90 minutes": "96",
                 "2 hours": "126"}


def translate_to_TMDB_params(session):
    """Takes user preferences and formats for TMDB API call."""
    tmdb_params = {
        "api_key": TMDB_API_KEY,
        "include_adult": False,
        "with_original_language": "en",
        "sort_by": "vote_average.desc",
        "vote_count.gte": "346",
        "with_runtime.gte": "59"
    }

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
        if len(session.genre) > 1:
            tmdb_params["vote_count.gte"] = "15"

    if session.runtime:
        tmdb_params["with_runtime.lte"] = TMDB_RUNTIMES[session.runtime]

    return tmdb_params


def get_recommendations(session_id):
    """Takes the id for a current session, makes a call to TMDB API, and stores 10 pages of results in database."""
    session = Session.query.get(session_id)
    tmdb_params = translate_to_TMDB_params(session)

    # Get 10 pages of results from TMDB. Add all movies to the database, identifiable by session_id.
  
    for i in range(1, 11):
        tmdb_params["page"] = str(i)
        response = requests.get(TMDB_PATH, params=tmdb_params)
        response = response.json()
        for movie in response["results"]:
            new_movie = Movie(
                tmdb_id=int(movie["id"]),
                title=movie["original_title"],
                overview=movie["overview"],
                release_date=movie["release_date"],
                poster=movie["poster_path"],
                session_id=session_id
            )
            db.session.add(new_movie)
            db.session.commit()

    return


def get_random_movie(session_id):
    """Takes a session id, queries the database, and returns a random movie in dictionary form."""

    # Get all movies from database with session ID
    session = Session.query.get(session_id)
    movie_recs = []
    for movie in session.movies:
        movie_recs.append({
            "id": movie.tmdb_id,
            "title": movie.title,
            "overview": movie.overview,
            "release_date": movie.release_date,
            "poster": movie.poster
        })

    random_num = random.randint(0, len(movie_recs))
    random_movie = movie_recs[random_num]

    return random_movie
