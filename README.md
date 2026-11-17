# ShelfTrack: Bookstore Inventory Management System 📚🗄️

> A command-line relational database application built in Python and SQLite3 for managing bookstore inventory, author records, and stock availability[cite: 18, 20, 22].

---

## 📋 Project Overview
Developed as a Databases Capstone Project, **ShelfTrack** is a modular CLI tool designed for bookstore clerks to manage book stock and author metadata[cite: 18, 19, 20, 22]. The system uses a normalized relational SQLite database (`ebookstore.db`) with foreign key constraints, `INNER JOIN` queries, input validation, and parameterized SQL statements to ensure data integrity and prevent SQL injection[cite: 18, 23].

---

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Database:** SQLite3 (Python standard library `sqlite3`)[cite: 18, 23]
* **Concepts Demonstrated:** Relational schema design, Foreign Keys (`ON DELETE CASCADE`), `INNER JOIN`, CRUD operations, Context Managers (`with` statements), Input Validation, Parameterized Queries[cite: 18, 23]

---

## 🗄️ Database Schema
The application automatically initializes and populates `ebookstore.db` with two relational tables on first run:

### 1. `author` Table
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY` | Unique 4-digit author identifier[cite: 18] |
| `name` | `TEXT` | `NOT NULL` | Full name of the author[cite: 18] |
| `country` | `TEXT` | `NOT NULL` | Author's country of origin[cite: 18, 22] |

### 2. `book` Table
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY` | Unique 4-digit book identifier[cite: 18] |
| `title` | `TEXT` | `NOT NULL` | Title of the book[cite: 18] |
| `authorID` | `INTEGER` | `NOT NULL`, `FOREIGN KEY` | References `author(id)` with `ON DELETE CASCADE`[cite: 18] |
| `qty` | `INTEGER` | `NOT NULL` | Available stock quantity[cite: 18, 20] |

---

## ✨ Key Features
* **Automated Database Seeding:** Checks for existing tables and populates default classic titles and authors if the database is empty[cite: 18].
* **Add New Books (`book_entry`):** Validates 4-digit IDs, prevents duplicate primary keys, and prompts to register new authors on the fly if an `authorID` does not yet exist[cite: 18].
* **Update Records (`update_book`):** Uses an `INNER JOIN` to display current book and author information before allowing updates to stock quantity, book title, or author details[cite: 18, 23].
* **Delete Books (`delete_book`):** Verifies record existence and requires user confirmation before removing entries[cite: 18].
* **Search Inventory (`search_books`):** Supports exact lookups by 4-digit Book ID or partial substring matching by title (`LIKE %query%`)[cite: 18].
* **Full Catalog View (`view_all_details`):** Joins `book` and `author` records and formats titles, author names, and countries using Python's `zip()` function[cite: 18, 22].
* **Defensive Coding:** Enforces 4-digit integer checks on IDs, non-negative integer checks on quantities, and automatic connection cleanup via `with` context managers[cite: 18, 23].

---

## 📂 Project Structure
```text
shelf-track/
│
├── self_track.py      # Main application script containing DB setup, validation & CLI menu[cite: 18]
├── ebookstore.db      # SQLite database file (auto-generated on first execution)[cite: 18]
└── README.md          # Project documentation
