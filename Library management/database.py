# database.py
import sqlite3

class Database:
    """
    A class to manage database operations for the library application.
    Uses SQLite to store book information.
    """
    def __init__(self, db_name="library.db"):
        """
        Initializes the Database object and connects to the SQLite database.
        Creates the 'books' table if it doesn't already exist.
        """
        self.conn = None
        self.cursor = None
        self.db_name = db_name
        self._connect()
        self._create_table()

    def _connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            # In a real application, you might want to log this error
            # or show a user-friendly message.

    def _create_table(self):
        """Creates the 'books' table if it does not exist."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT UNIQUE NOT NULL,
                    quantity INTEGER NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_book(self, title, author, isbn, quantity):
        """
        Inserts a new book record into the database.
        Returns True on success, False otherwise.
        """
        try:
            self.cursor.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)",
                                (title, author, isbn, quantity))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Error: Book with ISBN '{isbn}' already exists.")
            return False
        except sqlite3.Error as e:
            print(f"Error inserting book: {e}")
            return False

    def view_books(self, query=""):
        """
        Retrieves all book records from the database, or filters by a query.
        Returns a list of tuples, where each tuple represents a book record.
        """
        try:
            if query:
                # Search by title, author, or ISBN
                self.cursor.execute("""
                    SELECT * FROM books WHERE
                    title LIKE ? OR author LIKE ? OR isbn LIKE ?
                """, (f"%{query}%", f"%{query}%", f"%{query}%"))
            else:
                self.cursor.execute("SELECT * FROM books")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error viewing books: {e}")
            return []

    def update_book(self, id, title, author, isbn, quantity):
        """
        Updates an existing book record in the database.
        Returns True on success, False otherwise.
        """
        try:
            self.cursor.execute("UPDATE books SET title=?, author=?, isbn=?, quantity=? WHERE id=?",
                                (title, author, isbn, quantity, id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Error: Cannot update to ISBN '{isbn}', it already exists for another book.")
            return False
        except sqlite3.Error as e:
            print(f"Error updating book: {e}")
            return False

    def delete_book(self, id):
        """
        Deletes a book record from the database by its ID.
        Returns True on success, False otherwise.
        """
        try:
            self.cursor.execute("DELETE FROM books WHERE id=?", (id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting book: {e}")
            return False

    def __del__(self):
        """
        Closes the database connection when the Database object is destroyed.
        """
        if self.conn:
            self.conn.close()

# Example usage (for testing the module independently)
if __name__ == "__main__":
    db = Database("test_library.db")

    # Clear existing data for a clean test
    db.cursor.execute("DROP TABLE IF EXISTS books")
    db._create_table()

    print("Inserting books...")
    db.insert_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", 5)
    db.insert_book("1984", "George Orwell", "978-0451524935", 3)
    db.insert_book("To Kill a Mockingbird", "Harper Lee", "978-0061120084", 7)

    print("\nViewing all books:")
    for book in db.view_books():
        print(book)

    print("\nSearching for 'Gatsby':")
    for book in db.view_books("Gatsby"):
        print(book)

    print("\nUpdating '1984' quantity to 10:")
    # Assuming ID 2 for 1984 from previous insert
    books = db.view_books("1984")
    if books:
        book_id = books[0][0]
        db.update_book(book_id, "1984", "George Orwell", "978-0451524935", 10)
    for book in db.view_books():
        print(book)

    print("\nDeleting 'The Great Gatsby':")
    books = db.view_books("The Great Gatsby")
    if books:
        book_id = books[0][0]
        db.delete_book(book_id)
    for book in db.view_books():
        print(book)

    del db # Explicitly close connection for test
