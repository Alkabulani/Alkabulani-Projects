# ui.py
import tkinter as tk
from tkinter import messagebox, scrolledtext

class LibraryUI:
    """
    A class to manage the Graphical User Interface (GUI) for the library application.
    Uses Tkinter for creating windows, widgets, and handling user input.
    """
    def __init__(self, root, app_logic):
        """
        Initializes the LibraryUI object.

        Args:
            root (tk.Tk): The main Tkinter window.
            app_logic: An instance of the main application logic class (e.g., LibraryApp).
                       This is used to call methods that interact with the database.
        """
        self.root = root
        self.app_logic = app_logic
        self.root.title("Library Management System")
        self.root.geometry("800x600") # Set a default window size
        self.root.resizable(True, True) # Allow resizing

        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=0) # For labels/entries
        self.root.grid_rowconfigure(1, weight=0) # For buttons
        self.root.grid_rowconfigure(2, weight=1) # For listbox
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        self._create_widgets()

    def _create_widgets(self):
        """Creates all the GUI widgets (labels, entries, buttons, listbox)."""
        # --- Input Fields ---
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.grid(row=0, column=0, columnspan=4, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1) # Make entry fields expand

        # Title
        tk.Label(input_frame, text="Title:").grid(row=0, column=0, sticky="w", pady=2)
        self.title_text = tk.StringVar()
        self.title_entry = tk.Entry(input_frame, textvariable=self.title_text, width=50)
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        # Author
        tk.Label(input_frame, text="Author:").grid(row=1, column=0, sticky="w", pady=2)
        self.author_text = tk.StringVar()
        self.author_entry = tk.Entry(input_frame, textvariable=self.author_text, width=50)
        self.author_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        # ISBN
        tk.Label(input_frame, text="ISBN:").grid(row=0, column=2, sticky="w", padx=(20,0), pady=2)
        self.isbn_text = tk.StringVar()
        self.isbn_entry = tk.Entry(input_frame, textvariable=self.isbn_text, width=30)
        self.isbn_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=2)

        # Quantity
        tk.Label(input_frame, text="Quantity:").grid(row=1, column=2, sticky="w", padx=(20,0), pady=2)
        self.quantity_text = tk.StringVar()
        self.quantity_entry = tk.Entry(input_frame, textvariable=self.quantity_text, width=30)
        self.quantity_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=2)

        # --- Buttons ---
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.grid(row=1, column=0, columnspan=4, sticky="ew")
        for i in range(5): # 5 buttons, distribute horizontally
            button_frame.grid_columnconfigure(i, weight=1)

        tk.Button(button_frame, text="Add Book", command=self._add_command, width=15, relief=tk.RAISED, bd=3).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="View All", command=self._view_command, width=15, relief=tk.RAISED, bd=3).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Search Book", command=self._search_command, width=15, relief=tk.RAISED, bd=3).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Update Selected", command=self._update_command, width=15, relief=tk.RAISED, bd=3).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(button_frame, text="Delete Selected", command=self._delete_command, width=15, relief=tk.RAISED, bd=3).grid(row=0, column=4, padx=5, pady=5)

        # --- Book Listbox ---
        list_frame = tk.Frame(self.root, padx=10, pady=10)
        list_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        self.books_list = scrolledtext.ScrolledText(list_frame, height=15, width=80, wrap=tk.WORD, font=("Courier New", 10))
        self.books_list.grid(row=0, column=0, sticky="nsew")
        self.books_list.bind('<<Selection>>', self._on_list_select) # Bind selection event

        # Status message area
        self.status_message = tk.StringVar()
        self.status_label = tk.Label(self.root, textvariable=self.status_message, fg="blue", font=("Arial", 10, "italic"))
        self.status_label.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=5)

    def _clear_entries(self):
        """Clears the text in all input entry fields."""
        self.title_text.set("")
        self.author_text.set("")
        self.isbn_text.set("")
        self.quantity_text.set("")

    def _display_message(self, message, is_error=False):
        """Displays a message in the status bar."""
        self.status_message.set(message)
        self.status_label.config(fg="red" if is_error else "blue")

    def _on_list_select(self, event):
        """
        Event handler for when an item is selected in the listbox.
        Populates the entry fields with the selected book's details.
        """
        try:
            # Get the current selection indices
            indices = self.books_list.tag_ranges("sel")
            if not indices:
                return # No selection

            # Get the selected text
            selected_text = self.books_list.get(indices[0], indices[1])

            # Extract data. This assumes a consistent format from _display_books.
            # A more robust solution might involve storing IDs directly in the listbox
            # or using a Treeview widget.
            lines = selected_text.strip().split('\n')
            if not lines: return

            # Find the line containing "ID:"
            book_data = {}
            for line in lines:
                if "ID:" in line:
                    book_data["id"] = line.split("ID:")[1].strip().split(" ")[0]
                elif "Title:" in line:
                    book_data["title"] = line.split("Title:")[1].strip()
                elif "Author:" in line:
                    book_data["author"] = line.split("Author:")[1].strip()
                elif "ISBN:" in line:
                    book_data["isbn"] = line.split("ISBN:")[1].strip()
                elif "Quantity:" in line:
                    book_data["quantity"] = line.split("Quantity:")[1].strip()

            if book_data:
                self.selected_book_id = book_data.get("id")
                self.title_text.set(book_data.get("title", ""))
                self.author_text.set(book_data.get("author", ""))
                self.isbn_text.set(book_data.get("isbn", ""))
                self.quantity_text.set(book_data.get("quantity", ""))

        except Exception as e:
            self._display_message(f"Error selecting item: {e}", is_error=True)
            self.selected_book_id = None # Reset selected ID on error

    def _display_books(self, books):
        """
        Clears the listbox and populates it with the provided list of books.
        Each book is formatted for display.
        """
        self.books_list.delete(1.0, tk.END) # Clear existing content
        if not books:
            self.books_list.insert(tk.END, "No books found.\n")
            return

        for book in books:
            # book is a tuple: (id, title, author, isbn, quantity)
            self.books_list.insert(tk.END, f"----------------------------------------\n")
            self.books_list.insert(tk.END, f"ID: {book[0]}\n")
            self.books_list.insert(tk.END, f"Title: {book[1]}\n")
            self.books_list.insert(tk.END, f"Author: {book[2]}\n")
            self.books_list.insert(tk.END, f"ISBN: {book[3]}\n")
            self.books_list.insert(tk.END, f"Quantity: {book[4]}\n")
            self.books_list.insert(tk.END, f"----------------------------------------\n\n")

    # --- Command Handlers (Delegating to app_logic) ---
    def _add_command(self):
        """Handles the 'Add Book' button click."""
        title = self.title_text.get().strip()
        author = self.author_text.get().strip()
        isbn = self.isbn_text.get().strip()
        quantity_str = self.quantity_text.get().strip()

        if not all([title, author, isbn, quantity_str]):
            self._display_message("All fields must be filled.", is_error=True)
            return

        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")
        except ValueError:
            self._display_message("Quantity must be a non-negative integer.", is_error=True)
            return

        success = self.app_logic.add_book(title, author, isbn, quantity)
        if success:
            self._display_message("Book added successfully!")
            self._clear_entries()
            self.app_logic.view_all_books() # Refresh list
        else:
            self._display_message("Failed to add book. ISBN might already exist.", is_error=True)

    def _view_command(self):
        """Handles the 'View All' button click."""
        self.app_logic.view_all_books()
        self._display_message("Displaying all books.")
        self._clear_entries() # Clear entries after viewing all

    def _search_command(self):
        """Handles the 'Search Book' button click."""
        search_term = self.title_text.get().strip() # Use title field for search term
        if not search_term:
            self._display_message("Please enter a search term in the Title field.", is_error=True)
            return
        self.app_logic.search_books(search_term)
        self._display_message(f"Searching for '{search_term}'.")

    def _update_command(self):
        """Handles the 'Update Selected' button click."""
        if not hasattr(self, 'selected_book_id') or not self.selected_book_id:
            self._display_message("Please select a book from the list to update.", is_error=True)
            return

        title = self.title_text.get().strip()
        author = self.author_text.get().strip()
        isbn = self.isbn_text.get().strip()
        quantity_str = self.quantity_text.get().strip()

        if not all([title, author, isbn, quantity_str]):
            self._display_message("All fields must be filled for update.", is_error=True)
            return

        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")
        except ValueError:
            self._display_message("Quantity must be a non-negative integer.", is_error=True)
            return

        success = self.app_logic.update_book(self.selected_book_id, title, author, isbn, quantity)
        if success:
            self._display_message(f"Book ID {self.selected_book_id} updated successfully!")
            self._clear_entries()
            self.app_logic.view_all_books() # Refresh list
            self.selected_book_id = None # Deselect
        else:
            self._display_message("Failed to update book. ISBN might already exist for another book.", is_error=True)

    def _delete_command(self):
        """Handles the 'Delete Selected' button click."""
        if not hasattr(self, 'selected_book_id') or not self.selected_book_id:
            self._display_message("Please select a book from the list to delete.", is_error=True)
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete book ID {self.selected_book_id}?"):
            success = self.app_logic.delete_book(self.selected_book_id)
            if success:
                self._display_message(f"Book ID {self.selected_book_id} deleted successfully!")
                self._clear_entries()
                self.app_logic.view_all_books() # Refresh list
                self.selected_book_id = None # Deselect
            else:
                self._display_message("Failed to delete book.", is_error=True)

    def run(self):
        """Starts the Tkinter event loop."""
        self.root.mainloop()

# Example usage (for testing the module independently)
if __name__ == "__main__":
    # This is a mock AppLogic for UI testing purposes
    class MockAppLogic:
        def add_book(self, title, author, isbn, quantity):
            print(f"Mock: Adding {title} by {author} ({isbn}) Qty: {quantity}")
            return True

        def view_all_books(self):
            print("Mock: Viewing all books.")
            # Simulate some data
            self.ui._display_books([
                (1, "Mock Book 1", "Mock Author A", "111-222", 5),
                (2, "Mock Book 2", "Mock Author B", "333-444", 3)
            ])

        def search_books(self, query):
            print(f"Mock: Searching for '{query}'")
            self.ui._display_books([
                (1, "Mock Book 1", "Mock Author A", "111-222", 5)
            ])

        def update_book(self, id, title, author, isbn, quantity):
            print(f"Mock: Updating ID {id} to {title} by {author} ({isbn}) Qty: {quantity}")
            return True

        def delete_book(self, id):
            print(f"Mock: Deleting ID {id}")
            return True

    root = tk.Tk()
    mock_app = MockAppLogic()
    ui = LibraryUI(root, mock_app)
    mock_app.ui = ui # Link mock app to UI
    ui.run()
