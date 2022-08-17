# Matinee All Day (Backend)

Matinee All Day is a movie recommendation app created by Jodi Denney and Amel Ntamark as their capstone project for Ada Developer's Academy. This repo contains the backend logic for the app.

[View the deployed project here].(http://all-day-matinee.herokuapp.com/)

[View the frontend repo here].(https://github.com/J-J-D/Capstone)

## Setup

1. Git clone to your machine
2. run `python3 -m venv venv` to setup virtual environment
3. run `source venv/bin/activate` to activate virtual environment
4. run `pip install -r requirements.txt` to install requirements
5. In the project root, create a .env file and add the value `TMDB_API_KEY = {your_tmbd_api_key here}`, using your own API key from https://www.themoviedb.org/
6. Replicate the PostgreSQL database on your local machine.

## Getting a random movie

1. Start your flask server
2. Make a POST request to /sessions to save preferences.
3. Make a PUT request to /sessions/{session_id} to store movie results in the database.
4. Make a GET request to /sessions/{session_id} to receive a single instance of a movie recommendation.

## More features

- Users can be "logged in" by making a POST request to /users/login and providing a username in the JSON request body.

- Logged in users can add movies to their seen lists by making a PATCH request to /users/{user_id}/{tmdb_movie_id}

- Session info can be deleted from the database by making a DELETE request to /sessions/{session_id}

- Movie data can be deleted from the database by making a DELETE request to /sessions/movies
