from sqlalchemy import create_engine, text
import requests
from sqlalchemy.engine import row

API_URL = "https://www.omdbapi.com/"
API_KEY = "7367edc7"
MOVIE_DB_URL = "sqlite:///data/movies.db"
USER_DB_URL = "sqlite:///data/users.db"


# Create movie engine
movie_engine = create_engine(MOVIE_DB_URL) #echo=True to see what SQL does

# Create the movies table if it does not exist
with movie_engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT,
            imdb_id TEXT
        )
    """))
    connection.commit()

user_engine = create_engine(USER_DB_URL)

#Create the user table if it doesn't already exist
with user_engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL
        )
    """))
    connection.commit()


def list_users():
    """Retrieve all users from user database"""
    with user_engine.connect() as conn:
        result = conn.execute(text("SELECT user_id, first_name FROM users"))
        users = result.fetchall()

    return {row[0]: row[1] for row in users}


def add_user(first_name):
    """Add a new user to the database."""
    with user_engine.connect() as conn:
        try:
            conn.execute(text("INSERT INTO users (first_name) VALUES (:first_name)"),
                               {"first_name": first_name})
            conn.commit()
            print(f"User '{first_name}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def list_movies(user_id):
    """Retrieve all movies from the database."""
    with movie_engine.connect() as conn:
        result = conn.execute(text("SELECT user_id, title, year, rating, poster_url FROM movies WHERE user_id = :user_id"),
                        {"user_id": user_id})

        movies = result.fetchall()

    return {row[1]: {"user_id": row[0], "year": row[2], "rating": row[3], "poster_url": row[4]} for row in movies}


def add_movie(user_id, title):
    """Fetch movie data from OMDb and add it to the database"""
    params = {
        "apikey": API_KEY,
        "t": title
    }
    #Checking if the API request gets status 200 OK
    response = requests.get(API_URL, params=params)
    if response.status_code != 200:
        print("API request failed")
        return

    #Checking if movie exists
    data = response.json()
    if data.get("Response") == "False":
        print("Movie not found")
        return

    try:
        year = int(data["Year"])
        rating = float(data["imdbRating"])
        imdb_id = data.get("imdbID")
        poster_url = f"https://img.omdbapi.com/?apikey={API_KEY}&i={imdb_id}" if imdb_id else None
    except (KeyError, ValueError):
        print("Invalid data from API")
        return

    with movie_engine.connect() as conn:
        try:
            conn.execute(text("INSERT INTO movies (user_id, title, year, rating, poster_url, imdb_id) VALUES (:user_id, :title, :year, :rating, :poster_url, :imdb_id)"),
                               {"user_id": user_id, "title": title, "year": year, "rating": rating, "poster_url": poster_url, "imdb_id": imdb_id})
            conn.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(user_id, title):
    """Delete a movie from the database."""
    with movie_engine.connect() as conn:
        result = conn.execute(
            text("DELETE FROM movies WHERE title = :title AND user_id = :user_id"),
            {"user_id": user_id, "title": title}
        )
        conn.commit()

        if result.rowcount == 0:
            print(f"Movie '{title}' does not exist.")
        else:
            print(f"Movie '{title}' deleted successfully.")


def update_movie(user_id, title, rating):
    """Update a movie's rating in the database."""
    with movie_engine.connect() as conn:
        result = conn.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title AND user_id = :user_id"),
            {"user_id": user_id, "title": title, "rating": rating}
        )
        conn.commit()

        if result.rowcount == 0:
            print(f"Movie '{title}' does not exist.")
        else:
            print(f"Movie '{title}' updated successfully.")