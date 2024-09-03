import sqlite3
from dotenv import load_dotenv
import os
def init_db():
    load_dotenv()
    DATABASE_PATH = os.getenv('DATABASE_PATH')
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    # Create Categories table
    c.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # Create Payment Types table
    c.execute('''
    CREATE TABLE IF NOT EXISTS payment_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # Create Expenses table with expense_name column
    c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_name TEXT NOT NULL,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category_id INTEGER,
        payment_type_id INTEGER,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id),
        FOREIGN KEY (payment_type_id) REFERENCES payment_types (id)
    )
    ''')

    # Create Monthly Bills table (Optional based on your needs)
    """
    c.execute('''
    CREATE TABLE IF NOT EXISTS monthly_bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_name TEXT NOT NULL,
        amount REAL NOT NULL,
        due_date TEXT NOT NULL
    )
    ''')"""
    c.execute('''
        CREATE TABLE IF NOT EXISTS monthly_bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,
            bill_name TEXT NOT NULL,
            amount REAL NOT NULL,
            is_paid BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
