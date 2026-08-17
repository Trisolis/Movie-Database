# Flask and routing logic
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from api import API
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
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

# Specific movie page, based on the tmdb_id passed
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

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirects already logged in users away from page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Asks user for username, email, and password, and checks if validf
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        success = User.create(username, email, password)

        if not success:
            flash('Username or email already exists.', 'error')
            return render_template('register.html')

        # Redirect user where they were trying to go previously
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirects already logged in users away from page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Asks user for username and password, and checks if exists/information is right
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.get_by_username(username)

        if not user or not user.check_password(password):
            flash('Invalid username or password.', 'error')
            return render_template('login.html')

        # Redirect user where they were trying to go previously
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('home'))

    return render_template('login.html')

# Logout user, as long as they're currently logged in
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)