from sqlalchemy import create_engine, text
import requests

API_URL = "https://www.omdbapi.com/"
API_KEY = "7367edc7"
DB_URL = "sqlite:///movies.db"


# Create the engine
engine = create_engine(DB_URL) #echo=True to see what SQL does

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT,
            imdb_id TEXT
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]} for row in movies}


def add_movie(title):
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

    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster_url, imdb_id) VALUES (:title, :year, :rating, :poster_url, :imdb_id)"),
                               {"title": title, "year": year, "rating": rating, "poster_url": poster_url, "imdb_id": imdb_id})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title}
        )
        connection.commit()

        if result.rowcount == 0:
            print(f"Movie '{title}' does not exist.")
        else:
            print(f"Movie '{title}' deleted successfully.")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title"),
            {"title": title, "rating": rating}
        )
        connection.commit()

        if result.rowcount == 0:
            print(f"Movie '{title}' does not exist.")
        else:
            print(f"Movie '{title}' updated successfully.")