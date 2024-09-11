import bcrypt
import sqlite3

class User:
    def __init__(self, user_id, username, password_hash, first_name, last_name, email, phone, user_type):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.user_type = user_type

    def to_json(self):
        user_json = {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "user_type": self.user_type
        }
        return user_json

    def update_profile(self, **kwargs):
        """Update user profile information."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid profile attribute: {key}")

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def retrieve_checked_out_items(user_id):
    conn = sqlite3.connect('checked_out.db')
    cursor = conn.cursor()
    query = "SELECT name, author, type, publisher, checkout_date FROM checked_out_items WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    checked_out_items = cursor.fetchall()
    conn.close()

    return checked_out_items

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7])
    else:
        user = None

    return user

def all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    user_data = cursor.fetchall()
    users = []
    if user_data:
        for u in user_data:
            users.append(User(u[0], u[1], u[2], u[3], u[4], u[5], u[6]))
    conn.close()
    return users

def get_user_profile(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user_profile = {
            'username': user_data[1],
            'first_name': user_data[3],
            'last_name': user_data[4],
            'email': user_data[5],
            'phone': user_data[6]
        }
        return user_profile
    else:
        return None

def search_user_by_username(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user = User(*user_data)
    else:
        user = None

    return user

def search_user_by_librarian_id(librarian_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Query the database to find the user with the specified librarian ID
    query = "SELECT * FROM users WHERE id = ? AND user_type = 'librarian'"
    cursor.execute(query, (librarian_id,))
    
    # Fetch the user data if found
    user_data = cursor.fetchone()
    
    # Close the database connection
    conn.close()
    
    # If user_data is not None, create a User object and return it
    if user_data:
        user = User(*user_data)
        return user
    else:
        return None
