import sqlite3
import os
from dotenv import load_dotenv

def get_db_connection():
    load_dotenv()
    DATABASE_PATH = os.getenv('DATABASE_PATH')
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_category(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()
        print(f'Category "{name}" inserted successfully.')
    except sqlite3.IntegrityError:
        print(f'Category "{name}" already exists.')
    conn.close()

def insert_payment_type(type):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO payment_types (name) VALUES (?)', (type,))
        conn.commit()
        print(f'Payment type "{type}" inserted successfully.')
    except sqlite3.IntegrityError:
        print(f'Payment type "{type}" already exists.')
    conn.close()

def update_category(id, new_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE categories SET name = ? WHERE id = ?', (new_name, id))
    conn.commit()
    if cursor.rowcount > 0:
        print(f'Category ID {id} updated to "{new_name}".')
    else:
        print(f'Category ID {id} not found.')
    conn.close()

def update_payment_type(id, new_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE payment_types SET name = ? WHERE id = ?', (new_type, id))
    conn.commit()
    if cursor.rowcount > 0:
        print(f'Payment type ID {id} updated to "{new_type}".')
    else:
        print(f'Payment type ID {id} not found.')
    conn.close()


def delete_category(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categories WHERE id = ?', (id,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f'Category ID {id} deleted successfully.')
    else:
        print(f'Category ID {id} not found.')
    conn.close()


def delete_payment_type(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM payment_types WHERE id = ?', (id,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f'Payment type ID {id} deleted successfully.')
    else:
        print(f'Payment type ID {id} not found.')
    conn.close()

def get_category_by_name(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories WHERE name = ?', (name,))
    category = cursor.fetchall()
    conn.close()
    return category

def get_payment_type_by_name(type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payment_types WHERE name = ?', (type,))
    payment_type = cursor.fetchall()
    conn.close()
    return payment_type


def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories order by name asc', ())
    category = cursor.fetchall()
    conn.close()
    return category

def get_payment_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payment_types order by name asc', ())
    payment_type = cursor.fetchall()
    conn.close()
    return payment_type

if __name__ == "__main__":

    # Sample Inserts
    """insert_category('Credit Card Bill')
    insert_category('Monthly Expense')
    insert_category('Yearly Expense')
    insert_category('Mobile & Internet')
    insert_category('Medical')
    insert_category('Insurance')
    insert_category('Vehicle')
    insert_category('Food')
    insert_category('Kids')
    insert_category('Education')
    insert_category('Personal')
    insert_category('Groceries')
    insert_category('Memberships')
    insert_category('Travel')
    insert_category('Electrician')
    insert_category('Plumber')
    insert_category('Household')

    insert_payment_type('ICICI Bank Credit Card')
    insert_payment_type('Amazon ICICI Bank Credit Card')
    insert_payment_type('ICICI Bank')
    insert_payment_type('HDFC Bank Credit Card')
    insert_payment_type('HDFC Bank')
    insert_payment_type('IDFC Bank Credit Card')
    insert_payment_type('IDFC Bank')
    insert_payment_type('SBI Credit Card')
    insert_payment_type('SBI Bank')
    insert_payment_type('Yes Bank Credit Card')
    insert_payment_type('Amazon Pay Balance')
    insert_payment_type('Cash')"""

    # Sample Updates
    #update_category(1, 'Groceries')
    #update_payment_type(1, 'Debit Card')

    # Sample Deletes
    #delete_category(2)
    #delete_payment_type(2)

    # Fetch and print by name
    #category = get_category_by_name('Monthly Expense')
    #for r in category:
    #    print(r[0], r[1])

    #payment_type = get_payment_type_by_name('ICICI Bank')
    #for r in payment_type:
    #    print(r[0], r[1])

    categories = get_categories()
    for r in categories:
        print(r[0], r[1])

    payment_types = get_payment_types()
    for r in payment_types:
        print(r[0], r[1])