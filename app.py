# Flask and routing logic
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from api import API
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import User, bcrypt
from config import SECRET_KEY

app = Flask(__name__)
api = API()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt.init_app(app)

app.secret_key = SECRET_KEY

def get_db():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row # access by name instead of index
    return conn

# Home page, lists popular movies from the API
@app.route('/')
def home():
    movies = api.get_popular()
    return render_template('index.html', movies=movies)

# Search page, renders movies with user parameters applied
@app.route('/search')
def search():
    query = request.args.get('q')

    if not query:
        return redirect(url_for('home'))
    movies = api.search_movies(query)
    return render_template('search.html', movies=movies, query=query)

@app.route('/movie/<int:tmdb_id>')
def movie(tmdb_id):
    # Check local db first
    conn = get_db()
    local = conn.execute(
        'SELECT * FROM movies WHERE tmdb_id = ?', (tmdb_id,)
    ).fetchone()
    conn.close()

    # Fall back to API if not in database
    if local:
        details = dict(local)
    else:
        details = api.get_movie_details(tmdb_id)
        if not details:
            return render_template('404.html'), 404

    return render_template('movie.html', movie=details)

@app.route('/register', methods=['GET', 'POST'])
def register():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/logout')
@login_required
def logout():
    pass

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)