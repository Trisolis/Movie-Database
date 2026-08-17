# Handles sessions, password hashing, and authentication
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import sqlite3

bcrypt = Bcrypt()

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_id(user_id):
        conn = sqlite3.connect('movies.db')
        conn.row_factory = sqlite3.Row
        user = conn.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['email'], user['password_hash'], user['created_at'])
        return None

    @staticmethod
    def get_by_username(username):
        conn = sqlite3.connect('movies.db')
        conn.row_factory = sqlite3.Row
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['email'], user['password_hash'], user['created_at'])
        return None

    @staticmethod
    def create(username, email, password):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = sqlite3.connect('movies.db')
        try:
            conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', (username, email, password_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()