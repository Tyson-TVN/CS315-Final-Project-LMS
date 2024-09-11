import sqlite3

def init_checked_out_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('checked_out.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Execute the SQL command to create the table for checked out items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checked_out_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_id INTEGER,
            checkout_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            return_date TIMESTAMP
        );
    ''')

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
