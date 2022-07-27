import requests
import json

# ADD KEY BEFORE USING!
TMDB_PATH = "https://api.themoviedb.org/3/discover/movie"


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

    # each dictionary in response["results"] is a movie
    # each movie dictionary has a key called "title"

    for movie in response["results"]:
        movie_titles.append(movie["title"])

    print(f"response body: {movie_titles}")


get_horror_movie()
