# Movie-Database
A small app that allows users to create unique profiles, rate and search for movies from a database, and see their stats graphed and analyzed.

## Features
- 

## Setup (Building)
1. git clone ...
2. cd project
3. python -m venv venv
4. source venv/Scripts/activate
5. pip install -r requirements.txt
6. Create a 'config.py' file with: `API key="[your TMDB API key here]"` and `SECRET_KEY="[any random string]"`. Get a free key at https://www.themoviedb.org/settings/api
7. python schema.py
8. python.app.py
9. Visit http://127.0.0.1:5000

## Example Usage / Visuals

## Concepts Covered / Tech Stack
- User authentication with Flask-Login and password hashing with Flask-Bcrypt
- Session management and protected routes
- CRUD operations with SQLite
- External API consumption (TMDB)
- Relational database design with foreign keys
- Data visualization with Chart.js
- Responsive frontend with Bootstrap and Jinja2 templating

## API Reference
This project uses the [TMDB API](https://www.themoviedb.org/settings/api)
The application currently uses the following endpoints:
| Feature | TMDB Endpoint |
|---------|---------------|
| Feature 1 | Endpoint 1 |

## Demo
A demo account is available to explore the app without registering:
- Username: demo
- Password: demo123