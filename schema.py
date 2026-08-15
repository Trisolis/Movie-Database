# Creates the SQLite database and defines tables
import sqlite3

# Connect to db file, create a cursor to execute SQL queries
conn = sqlite3.connect("movies.db") # creates file if it doesn't exist
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON") # needed to enable foreign keys

# Creating multiple tables with executescript
cursor.executescript("""
    DROP TABLE IF EXISTS movies 
    DROP TABLE IF NOT EXISTS watchlists
    DROP TABLE IF NOT EXISTS users

    CREATE TABLE IF NOT EXISTS movies {
        
    };

    CREATE TABLE IF NOT EXISTS watchlists {

    };

    CREATE TABLE IF NOT EXISTS users {

    };
""")

# Commit changes and save to db file
conn.commit()
conn.close()

# users and movies don't intersect, but both intersect w watchlists