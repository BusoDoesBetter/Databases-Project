import sqlite3

def get_db_connection():
    """Establishes and returns a connection to the database."""
    # Returns a connection object that can be used with context managers
    return sqlite3.connect("ebookstore.db")


def create_tables():
    """Creates author and book tables if they don't exist and 
    populates default data."""

    with get_db_connection() as db:
        cursor = db.cursor()

        # Enable foreign key support to enforce referential integrity
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Create author table
        # name and country columns are NOT NULL because they cannot be empty
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
            );
        """
        )

        # Create book table
        # title, authorID and qty columns are NOT NULL because they cannot be empty
        # authorID is a foreign key that references the author table's id column
        # ON DELETE CASCADE ensures that if an author is deleted, their books are also deleted
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authorID INTEGER NOT NULL,
                qty INTEGER NOT NULL,
                FOREIGN KEY (authorID) REFERENCES author(id) ON DELETE CASCADE
            );
        """
        )

        # Check if author table is empty before populating with default data
        cursor.execute("SELECT COUNT(*) FROM author;")
        if cursor.fetchone()[0] == 0:
            # Initialize with 5 default authors
            default_authors = [
                (1290, "Charles Dickens", "England"),
                (8937, "J.K. Rowling", "England"),
                (2356, "C.S. Lewis", "Ireland"),
                (6380, "J.R.R. Tolkien", "South Africa"),
                (5620, "Lewis Carroll", "England"),
            ]
            # executemany() is more efficient than individual INSERT statements
            cursor.executemany(
                "INSERT INTO author (id, name, country) VALUES (?, ?, ?);",
                default_authors,
            )

        # Check if book table is empty before populating with default data
        cursor.execute("SELECT COUNT(*) FROM book;")
        if cursor.fetchone()[0] == 0:
            # Initialize with 5 default books
            default_books = [
                (3001, "A Tale of Two Cities", 1290, 30),
                (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
                (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
                (3004, "The Lord of the Rings", 6380, 37),
                (3005, "Alice's Adventures in Wonderland", 5620, 12),
            ]
            # executemany() inserts multiple rows in one operation
            cursor.executemany(
                "INSERT INTO book (id, title, authorID, qty) VALUES (?, ?, ?, ?);",
                default_books,
            )

        # Commit all changes to the database
        db.commit()


def validate_four_digit_id(entry):
    """Validates that user input is an integer exactly four digits long."""
    # Loop continues until valid input is received
    while True:
        user_input = input(entry).strip()
        # isdigit() checks if all characters are digits, len() checks it's exactly 4 characters
        if user_input.isdigit() and len(user_input) == 4:
            return int(user_input)
        # If validation fails, re-prompt user with error message
        print("Error: Input must be a positive 4-digit integer (e.g., 1234).")


def validate_positive_int(entry):
    """Validates that user input is a non-negative integer."""
    # Loop continues until valid input is received
    while True:
        user_input = input(entry).strip()
        # isdigit() ensures the input is a valid non-negative number
        if user_input.isdigit():
            return int(user_input)
        # If validation fails, re-prompt user with error message
        print("Error: Input must be a valid non-negative integer.")


def book_entry():
    """Prompts clerk to enter details for a new book and author if needed."""
    print("\n--- Enter New Book ---")
    # Get valid 4-digit book ID from user
    book_id = validate_four_digit_id("Enter 4-digit Book ID: ")

    with get_db_connection() as db:
        cursor = db.cursor()
        # Check if book ID already exists in database
        cursor.execute("SELECT id FROM book WHERE id = ?;", (book_id,))

        if cursor.fetchone():
            # If book exists, notify user and exit function
            print(f"Error: A book with ID {book_id} already exists.")
            return

        # Get book title from user and validate it's not empty
        title = input("Enter Book Title: ").strip()
        while not title:
            print("Title cannot be empty.")
            title = input("Enter Book Title: ").strip()

        # Get valid 4-digit author ID from user
        author_id = validate_four_digit_id("Enter 4-digit Author ID: ")

        # Check if author already exists in database
        cursor.execute("SELECT name, country FROM author WHERE id = ?;", (author_id,))
        author = cursor.fetchone()

        # If author doesn't exist, prompt user to add new author details
        if not author:
            print(f"Author ID {author_id} not found in system. Adding new author details.")
            name = input("Enter Author Name: ").strip()
            country = input("Enter Author Country: ").strip()
            # Insert new author into author table
            cursor.execute(
                "INSERT INTO author (id, name, country) VALUES (?, ?, ?);",
                (author_id, name, country),
            )
            print(f"Author '{name}' added successfully.")

        # Get book quantity from user with validation
        qty = validate_positive_int("Enter Quantity: ")

        # Insert new book into book table with all required information
        cursor.execute(
            "INSERT INTO book (id, title, authorID, qty) VALUES (?, ?, ?, ?);",
            (book_id, title, author_id, qty),
        )
        # Save changes to database
        db.commit()
        print(f"Book '{title}' added successfully!")


def update_book():
    """Updates quantity, title, or author information 
    for a specific book."""

    print("\n--- Update Book ---")
    # Get valid 4-digit book ID from user
    book_id = validate_four_digit_id("Enter 4-digit Book ID to update: ")

    with get_db_connection() as db:
        cursor = db.cursor()
        # INNER JOIN combines book and author data into one result
        # retrieves all information needed to display and update the book
        cursor.execute(
            """
            SELECT b.title, b.qty, a.id, a.name, a.country 
            FROM book b 
            INNER JOIN author a ON b.authorID = a.id 
            WHERE b.id = ?;
        """,
            (book_id,),
        )
        found = cursor.fetchone()

        # If book is not found, notify user and exit function
        if not found:
            print(f"Error: No book found with ID {book_id}.")
            return

        # Unpack the retrieved book information
        title, qty, author_id, author_name, author_country = found

        # Display current book information to user
        print(f"\nCurrent Details:")
        print(f"Title: {title} | Qty: {qty}")
        print(f"Author Name: {author_name} | Author Country: {author_country}")

        # Present update options to user
        print("\nWhat would you like to update?")
        print("1. Quantity (Default)")
        print("2. Title")
        print("3. Author Details (Name / Country)")
        choice = input("Enter choice (1-3) [Default 1]: ").strip()

        # Option 2: Update book title
        if choice == "2":
            new_title = input("Enter new title: ").strip()
            if new_title:
                # Update only the title column in the book table
                cursor.execute("UPDATE book SET title = ? WHERE id = ?;", (new_title, book_id))
                db.commit()
                print("Book title updated successfully.")
        # Option 3: Update author name and/or country
        elif choice == "3":
            new_name = input(f"Current Author name: {author_name}, enter new Author name or leave blank to keep current: ").strip()
            new_country = input(f"Current Author country: {author_country}, enter new Author country or leave blank to keep current]: ").strip()

            # If user enters new name, use it; otherwise keep current name
            if new_name:
                final_name = new_name 
            else: 
                final_name = author_name

            # If user enters new country, use it; otherwise keep current country
            if new_country:
                final_country = new_country  
            else: 
                final_country = author_country

            # Update author table with new information
            cursor.execute(
                "UPDATE author SET name = ?, country = ? WHERE id = ?;",
                (final_name, final_country, author_id),
            )
            db.commit()
            print("Author details updated successfully.")
        # Option 1 (or default): Update book quantity
        else:
            new_qty = validate_positive_int("Enter new quantity: ")
            # Update only the qty column in the book table
            cursor.execute("UPDATE book SET qty = ? WHERE id = ?;", (new_qty, book_id))
            db.commit()
            print("Book quantity updated successfully.")


def delete_book():
    """Deletes a book from the database by ID."""
    print("\n--- Delete Book ---")
    # Get valid 4-digit book ID from user
    book_id = validate_four_digit_id("Enter 4-digit Book ID to delete: ")

    with get_db_connection() as db:
        cursor = db.cursor()
        # Check if book exists before attempting deletion
        cursor.execute("SELECT title FROM book WHERE id = ?;", (book_id,))
        book = cursor.fetchone()

        # If book not found, notify user and exit function
        if not book:
            print(f"Error: No book found with ID {book_id}.")
            return

        # Ask user for confirmation before deleting
        confirm = input(f"Are you sure you want to delete '{book[0]}'? (y/n): ").strip().lower()
        if confirm == "y":
            # Delete the book from the database
            cursor.execute("DELETE FROM book WHERE id = ?;", (book_id,))
            # Save changes to database
            db.commit()
            print("Book deleted successfully.")
        else:
            print("Deletion canceled.")


def search_books():
    """Searches for a book by ID or title substring."""
    print("\n--- Search Books ---")
    # Get search term from user (can be book ID or partial title)
    search_item = input("Enter Book ID or Title to search: ").strip()

    with get_db_connection() as db:
        cursor = db.cursor()
        # INNER JOIN combines book and author data
        # WHERE clause uses OR to search by exact ID or partial title match
        # LIKE operator with % wildcards allows substring matching (e.g., "harry" finds "Harry Potter")
        cursor.execute(
            """
            SELECT b.id, b.title, a.name, b.qty 
            FROM book b 
            INNER JOIN author a ON b.authorID = a.id 
            WHERE b.id = ? OR b.title LIKE ?;
        """,
            (search_item, f"%{search_item}%"),
        )
        results = cursor.fetchall()

        # If no books match the search, inform user
        if not results:
            print("No matching books found.")
        else:
            # Display all matching books in a formatted table
            print("\nMatching Books:")
            print("-" * 50)
            for b_id, title, author_name, qty in results:
                print(f"ID: {b_id} | Title: {title} | Author: {author_name} | Qty: {qty}")
            print("-" * 50)


def view_all_details():
    """Fetches titles, author names, and countries using INNER JOIN and zip() as required."""
    with get_db_connection() as db:
        cursor = db.cursor()
        # INNER JOIN retrieves matching records from both book and author tables
        cursor.execute(
            """
            SELECT b.title, a.name, a.country 
            FROM book b 
            INNER JOIN author a ON b.authorID = a.id;
            """
        )
        records = cursor.fetchall()

        # If no records exist, inform user
        if not records:
            print("No books in the database.")
            return

        # Separate data into three lists: titles, author names, and countries
        titles = [row[0] for row in records]
        author_names = [row[1] for row in records]
        author_countries = [row[2] for row in records]

        # zip() combines the three lists element-by-element for iteration
        # This allows us to loop through all three lists simultaneously
        print("\nDetails")
        print("=" * 40)
        for title, name, country in zip(titles, author_names, author_countries):
            print(f"Title: {title}")
            print(f"Author's Name: {name}")
            print(f"Author's Country: {country}\n")


def display_menu():
    """Main menu display loop."""
    # Create tables and populate with default data on startup
    create_tables()

    # Display menu until user chooses to exit
    while True:
        print("\n" + "=" * 30)
        print("      EBOOKSTORE MENU      ")
        print("=" * 30)
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View details of all books")
        print("0. Exit")
        print("=" * 30)

        choice = input("Enter choice (0-5): ").strip()

        # Directs user to appropriate function based on menu choice
        if choice == "1":
            book_entry()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_books()
        elif choice == "5":
            view_all_details()
        elif choice == "0":
            print("Exiting ShelfTrack system. Goodbye!")
            # Exit the while loop to end the program
            break
        else:
            # Inform user if invalid choice is entered
            print("Invalid selection. Please enter a number from 0 to 5.")


#display_menu() only runs when script is executed directly
if __name__ == "__main__":
    display_menu()