# Creates the SQLite database and defines tables
import sqlite3
import requests
from config import API_KEY

# Connect to db file, create a cursor to execute SQL queries
conn = sqlite3.connect("movies.db") # creates file if it doesn't exist
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON") # needed to enable foreign keys

# Creating multiple tables with executescript
cursor.executescript("""
    DROP TABLE IF EXISTS movies;
    DROP TABLE IF EXISTS watchlists;
    DROP TABLE IF EXISTS users;

    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tmdb_id INTEGER UNIQUE,
        title TEXT NOT NULL,
        release_date TEXT,
        overview TEXT,
        tagline TEXT,
        poster_path TEXT,
        vote_average REAL,
        vote_count INTEGER,
        runtime INTEGER,
        genres TEXT,
        original_language TEXT
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS watchlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL, 
        status TEXT NOT NULL,
        rating REAL,
        review TEXT,
        date_watched TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (movie_id) REFERENCES movies(id)
    );
""")

# Seed ~1000 movies into the database so it's not just empty
def seed_movies(conn, pages=50):
    for page in range(1, pages+1):
        response = requests.get("https://api.themoviedb.org/3/movie/popular", 
                                params={"api_key": API_KEY, "page": page}
        )
        movies = response.json()["results"]
        for movie in movies:
            conn.execute("""
                INSERT OR IGNORE INTO movies (tmdb_id, title, release_date, overview, poster_path, vote_average, vote_count, original_language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                movie["id"],
                movie["title"],
                movie["release_date"],
                movie["overview"],
                movie["poster_path"],
                movie["vote_average"],
                movie["vote_count"],
                movie["original_language"]
            ))
    conn.commit()

seed_movies(conn)

# Commit changes and save to db file
conn.commit()
conn.close()