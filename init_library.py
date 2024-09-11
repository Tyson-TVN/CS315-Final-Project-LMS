# init_library.py

import sqlite3

def init_library_db():
    conn = sqlite3.connect('library_items.db')
    cursor = conn.cursor()

    # Create the library_items table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS library_items (
            ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            AuthorArtistDirector TEXT,
            PublisherLabelStudio TEXT,
            PublicationYearReleaseYear INTEGER,
            Type TEXT,
            AvailableStatus TEXT,
            Quantity INTEGER
        )
    ''')

    '''
    # Insert initial data
    cursor.execute(
        "INSERT INTO library_items (Title, AuthorArtistDirector, PublisherLabelStudio, PublicationYearReleaseYear, Type, AvailableStatus, Quantity) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ('Computer Science Textbook', 'James', 'Lion Publisher', None, 'Book', 'Available', 1))
         '''

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_library_db()
