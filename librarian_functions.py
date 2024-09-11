import sqlite3
import init_user

class Librarian:
    def _init_(self, librarian_id, username, password_hash, first_name, last_name, email, phone):
        self.id = librarian_id
        self.username = username
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

def add_librarian(username, password_hash, first_name, last_name, email, phone):
    

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, 'librarian')",
                   (username, password_hash, first_name, last_name, email, phone))
    conn.commit()
    conn.close()

def add_patron(username, password_hash, first_name, last_name, email, phone):
    

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, 'patron')",
                   (username, password_hash, first_name, last_name, email, phone))
    conn.commit()
    conn.close()

def search_items(title):
    conn = sqlite3.connect('library_items.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM library_items WHERE Title LIKE ?", ('%' + title + '%',))
    items_data = cursor.fetchall()
    items = []
    if items_data:
        for item_data in items_data:
            items.append({
                "ItemID": item_data[0],
                "Title": item_data[1],
                "AuthorArtistDirector": item_data[2],
                "PublisherLabelStudio": item_data[3],
                "PublicationYearReleaseYear": item_data[4],
                "Type": item_data[5],
                "AvailableStatus": item_data[6],
                "Quantity": item_data[7]
            })
    conn.close()
    return items

def add_library_item(title, author, publisher, publication_year, item_type, available_status, quantity):
    conn = sqlite3.connect('library_items.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO library_items (Title, AuthorArtistDirector, PublisherLabelStudio, PublicationYearReleaseYear, Type, AvailableStatus, Quantity) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (title, author, publisher, publication_year, item_type, available_status, quantity))
    conn.commit()
    conn.close()

def display_all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users_data = cursor.fetchall()
    users = []
    if users_data:
        for user_data in users_data:
            users.append({
                "id": user_data[0],
                "username": user_data[1],
                "password": user_data[2],
                "first_name": user_data[3],
                "last_name": user_data[4],
                "email": user_data[5],
                "phone": user_data[6],
                "user_type": user_data[7]
            })
    conn.close()
    return users

def search_user_by_username(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    user = None
    if user_data:
        user = {
            "id": user_data[0],
            "username": user_data[1],
            "password": user_data[2],
            "first_name": user_data[3],
            "last_name": user_data[4],
            "email": user_data[5],
            "phone": user_data[6],
            "user_type": user_data[7]
        }
    conn.close()
    return user


def display_user_checkout_items(library_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT i.* FROM checkouts AS c INNER JOIN library_items AS i ON c.item_id = i.ItemID WHERE c.user_id = ?", (library_id,))
    items_data = cursor.fetchall()
    items = []
    if items_data:
        for item_data in items_data:
            items.append({
                "ItemID": item_data[0],
                "Title": item_data[1],
                "AuthorArtistDirector": item_data[2],
                "PublisherLabelStudio": item_data[3],
                "PublicationYearReleaseYear": item_data[4],
                "Type": item_data[5],
                "AvailableStatus": item_data[6],
                "Quantity": item_data[7]
            })
    conn.close()
    return items

def retrieve_all_items():
    conn = sqlite3.connect('library_items.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM library_items")
    items_data = cursor.fetchall()
    items = []
    if items_data:
        for item_data in items_data:
            items.append({
                "ItemID": item_data[0],
                "Title": item_data[1],
                "AuthorArtistDirector": item_data[2],
                "PublisherLabelStudio": item_data[3],
                "PublicationYearReleaseYear": item_data[4],
                "Type": item_data[5],
                "AvailableStatus": item_data[6],
                "Quantity": item_data[7]
            })
    conn.close()
    return items

# Function to search items by title in the database
def search_item_by_title(title):
    conn = sqlite3.connect('library_items.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM library_items WHERE Title LIKE ?", ('%' + title + '%',))
    item_data = cursor.fetchone()
    item = None
    if item_data:
        item = {
            "ItemID": item_data[0],
            "Title": item_data[1],
            "AuthorArtistDirector": item_data[2],
            "PublisherLabelStudio": item_data[3],
            "PublicationYearReleaseYear": item_data[4],
            "Type": item_data[5],
            "AvailableStatus": item_data[6],
            "Quantity": item_data[7]
        }
    conn.close()
    return item


    import sqlite3

def retrieve_checked_out_items(user_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT i.Title, i.AuthorArtistDirector, c.CheckoutDate FROM checkouts AS c INNER JOIN library_items AS i ON c.item_id = i.ItemID WHERE c.user_id = ?", (user_id,))
    items_data = cursor.fetchall()
    conn.close()

    checked_out_items = []
    for item_data in items_data:
        checked_out_items.append({
            "title": item_data[0],
            "author": item_data[1],
            "checkout_date": item_data[2]
        })

    return checked_out_items
