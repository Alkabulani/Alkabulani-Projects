# app.py
import tkinter as tk
from database import Database
from ui import LibraryUI

class LibraryApp:
    """
    The main application logic for the Library Management System.
    Connects the UI (LibraryUI) with the database (Database).
    """
    def __init__(self, root):
        """
        Initializes the LibraryApp.

        Args:
            root (tk.Tk): The main Tkinter window.
        """
        self.db = Database("library.db") # Initialize the database connection
        self.ui = LibraryUI(root, self) # Initialize the UI, passing itself (this app) as logic handler
        self._initialize_data() # Optional: Add some initial data if database is empty

    def _initialize_data(self):
        """
        Adds some sample data if the database is empty.
        This is useful for first-time runs.
        """
        if not self.db.view_books(): # Check if any books exist
            print("Database is empty. Adding sample data...")
            self.db.insert_book("The Hobbit", "J.R.R. Tolkien", "978-0345339683", 10)
            self.db.insert_book("Pride and Prejudice", "Jane Austen", "978-0141439518", 7)
            self.db.insert_book("To the Lighthouse", "Virginia Woolf", "978-0156907392", 4)
            self.db.insert_book("Dune", "Frank Herbert", "978-0441013593", 6)
            self.db.insert_book("Foundation", "Isaac Asimov", "978-0553803717", 8)
            self.ui._display_message("Sample data added. Click 'View All' to see them.")
        else:
            self.ui._display_message("Database already contains books. Click 'View All' to display.")

    def add_book(self, title, author, isbn, quantity):
        """
        Adds a new book to the database.
        Delegates to the Database module.
        Returns True if successful, False otherwise.
        """
        return self.db.insert_book(title, author, isbn, quantity)

    def view_all_books(self):
        """
        Retrieves all books from the database and displays them in the UI.
        Delegates to the Database module for data, and UI for display.
        """
        books = self.db.view_books()
        self.ui._display_books(books)

    def search_books(self, query):
        """
        Searches for books in the database and displays the results in the UI.
        Delegates to the Database module for data, and UI for display.
        """
        books = self.db.view_books(query)
        self.ui._display_books(books)

    def update_book(self, book_id, title, author, isbn, quantity):
        """
        Updates an existing book in the database.
        Delegates to the Database module.
        Returns True if successful, False otherwise.
        """
        return self.db.update_book(book_id, title, author, isbn, quantity)

    def delete_book(self, book_id):
        """
        Deletes a book from the database.
        Delegates to the Database module.
        Returns True if successful, False otherwise.
        """
        return self.db.delete_book(book_id)

    def run(self):
        """Starts the Tkinter event loop."""
        self.ui.run()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    app.run()
