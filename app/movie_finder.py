import random
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


def translate_to_TMDB_params(session):
    """Take user preferences and format for TMDB API call."""
    tmdb_params = {
        "api_key": TMDB_API_KEY,
        "include_adult": False,
        # Could we give the user option to see film recommendations in other langs?
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

    return tmdb_params


def get_random_movie(json_response):
    """Returns a random movie from a JSON response"""
    random_num = random.randint(0, len(json_response["results"])-1)
    random_movie = json_response["results"][random_num]
    return random_movie
