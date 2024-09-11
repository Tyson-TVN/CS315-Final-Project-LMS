import sqlite3

class Patron:
    def __init__(self, patron_id, username, password_hash, first_name, last_name, email, phone):
        self.id = patron_id
        self.username = username
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

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

def checkout_item(user_id, item_id):
    conn = sqlite3.connect('library_items.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO checked_out_items (user_id, item_id) VALUES (?, ?)", (user_id, item_id))
        cursor.execute("UPDATE library_items SET AvailableStatus = 'Checked Out' WHERE ItemID = ?", (item_id,))
        conn.commit()
        print("Item checked out successfully!")
    except sqlite3.Error as e:
        print("Error occurred while checking out item:", e)
    finally:
        conn.close()

def display_checked_out_items(user_id):
    conn = sqlite3.connect('library_items.db')
    cursor = conn.cursor()
    cursor.execute("SELECT i.* FROM checked_out_items AS c INNER JOIN library_items AS i ON c.item_id = i.ItemID WHERE c.user_id = ?", (user_id,))
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
