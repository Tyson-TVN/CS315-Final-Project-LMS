# init_user.py

import sqlite3
import bcrypt

def init_user_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            user_type TEXT 
        )
    ''')

    # Insert initial data for librarian and patron
    password1_hash = bcrypt.hashpw(b'secret1', bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ('librarian1', password1_hash, 'John', 'Doe', 'john.doe@example.com', '123-456-7890', 'librarian'))  # Added 'librarian' as user_type
    password2_hash = bcrypt.hashpw(b'secret2', bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ('patron1', password2_hash, 'Jane', 'Smith', 'jane.smith@example.com', '987-654-3210', 'patron'))  # Added 'patron' as user_type

    conn.commit()
    conn.close()

if __name__ == '__main__':
    sys_init()
