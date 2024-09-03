from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
app = Flask(__name__)

# Database connection
def get_db_connection():
    load_dotenv()
    DATABASE_PATH = os.getenv('DATABASE_PATH')
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Add Expense
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    conn = get_db_connection()
    c = conn.cursor()

    if request.method == 'POST':
        expense_name = request.form['expense_name']
        date = request.form['date']
        amount = request.form['amount']
        category_id = request.form['category']
        payment_type_id = request.form['payment_type']
        description = request.form['description']

        c.execute('''
        INSERT INTO expenses (expense_name, date, amount, category_id, payment_type_id, description)
        VALUES (?, ?, ?, ?, ?, ?)''', (expense_name, date, amount, category_id, payment_type_id, description))

        conn.commit()
        conn.close()
        return redirect(url_for('view_expenses'))

    categories = c.execute('SELECT * FROM categories order by name asc').fetchall()
    payment_types = c.execute('SELECT * FROM payment_types order by name asc').fetchall()
    conn.close()

    return render_template('add_expense.html', categories=categories, payment_types=payment_types)

# View Expenses
@app.route('/view_expenses')
def view_expenses():
    conn = get_db_connection()
    expenses = conn.execute('''
    SELECT e.id, e.expense_name, e.date, e.amount, c.name AS category, p.name AS payment_type, e.description
    FROM expenses e
    LEFT JOIN categories c ON e.category_id = c.id
    LEFT JOIN payment_types p ON e.payment_type_id = p.id
    ''').fetchall()
    conn.close()

    return render_template('view_expenses.html', expenses=expenses)

# Summary
@app.route('/summary')
def summary():
    conn = get_db_connection()
    total_amount = conn.execute('SELECT SUM(amount) AS total FROM expenses').fetchone()['total']

    category_totals = conn.execute('''
    SELECT c.name AS category, SUM(e.amount) AS total
    FROM expenses e
    LEFT JOIN categories c ON e.category_id = c.id
    GROUP BY c.name
    ''').fetchall()

    payment_type_totals = conn.execute('''
    SELECT p.name AS payment_type, SUM(e.amount) AS total
    FROM expenses e
    LEFT JOIN payment_types p ON e.payment_type_id = p.id
    GROUP BY p.name
    ''').fetchall()

    conn.close()

    return render_template('summary.html', total_amount=total_amount,
                           category_totals={row['category']: row['total'] for row in category_totals},
                           payment_type_totals={row['payment_type']: row['total'] for row in payment_type_totals})

# Add Category
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    conn = get_db_connection()
    if request.method == 'POST':
        category_name = request.form['name']
        conn.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
        conn.commit()
        conn.close()
        return redirect(url_for('add_expense'))

    conn.close()
    return render_template('add_category.html')

# Add Payment Type
@app.route('/add_payment_type', methods=['GET', 'POST'])
def add_payment_type():
    conn = get_db_connection()
    if request.method == 'POST':
        payment_type_name = request.form['name']
        conn.execute('INSERT INTO payment_types (name) VALUES (?)', (payment_type_name,))
        conn.commit()
        conn.close()
        return redirect(url_for('add_expense'))

    conn.close()
    return render_template('add_payment_type.html')

# Monthly Bills
"""
@app.route('/monthly_bills', methods=['GET', 'POST'])
def monthly_bills():
    conn = get_db_connection()

    if request.method == 'POST':
        bill_name = request.form['bill_name']
        amount = request.form['amount']
        due_date = request.form['due_date']
        conn.execute('''
        INSERT INTO monthly_bills (bill_name, amount, due_date)
        VALUES (?, ?, ?)''', (bill_name, amount, due_date))

        conn.commit()
        return redirect(url_for('monthly_bills'))

    bills = conn.execute('SELECT * FROM monthly_bills').fetchall()
    conn.close()

    return render_template('monthly_bills.html', bills=bills)
"""


@app.route('/monthly_bills', methods=['GET', 'POST'])
def monthly_bills():
    conn = get_db_connection()

    if request.method == 'POST':
        month = request.form['month']
        bill_name = request.form['bill_name']
        amount = request.form['amount']
        conn.execute('INSERT INTO monthly_bills (month, bill_name, amount) VALUES (?, ?, ?)',
                     (month, bill_name, amount))
        conn.commit()

    # Get current month and year
    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    # Fetch bills and update their status based on expenses
    bills = conn.execute('SELECT * FROM monthly_bills ORDER BY month').fetchall()
    for bill in bills:
        expenses = conn.execute('SELECT * FROM expenses WHERE expense_name = ? AND strftime("%Y-%m", date) = ?',
                                (bill['bill_name'], bill['month'])).fetchall()
        is_paid = any(expense['date'] is not None for expense in expenses)
        conn.execute('UPDATE monthly_bills SET is_paid = ? WHERE id = ?', (is_paid, bill['id']))

    conn.commit()
    bills = conn.execute(
        'SELECT * FROM monthly_bills ORDER BY month').fetchall()  # Refresh the list with updated paid statuses
    conn.close()

    return render_template('monthly_bills.html', bills=bills, current_month=current_month)

# Update Bill Status
@app.route('/update_bill_status/<int:bill_id>', methods=['POST'])
def update_bill_status(bill_id):
    conn = get_db_connection()
    is_paid = request.form.get('is_paid', 'off') == 'on'
    conn.execute('UPDATE monthly_bills SET is_paid = ? WHERE id = ?', (is_paid, bill_id))
    conn.commit()
    conn.close()
    return redirect(url_for('monthly_bills'))

# Edit Expense
@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    conn = get_db_connection()
    c = conn.cursor()

    if request.method == 'POST':
        expense_name = request.form['expense_name']
        date = request.form['date']
        amount = request.form['amount']
        category_id = request.form['category']
        payment_type_id = request.form['payment_type']
        description = request.form['description']

        c.execute('''
        UPDATE expenses
        SET expense_name = ?, date = ?, amount = ?, category_id = ?, payment_type_id = ?, description = ?
        WHERE id = ?''', (expense_name, date, amount, category_id, payment_type_id, description, expense_id))

        conn.commit()
        conn.close()
        return redirect(url_for('view_expenses'))

    # Fetch the current details of the expense to populate the form
    expense = c.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,)).fetchone()
    categories = c.execute('SELECT * FROM categories').fetchall()
    payment_types = c.execute('SELECT * FROM payment_types').fetchall()
    conn.close()

    return render_template('edit_expense.html', expense=expense, categories=categories, payment_types=payment_types)

# Delete Expense
@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_expenses'))

# Generate Monthly spending chart
def generate_monthly_spending_chart():
    conn = get_db_connection()
    monthly_data = conn.execute('''
    SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total
    FROM expenses
    GROUP BY month
    ORDER BY month DESC
    ''').fetchall()
    conn.close()

    months = [row['month'] for row in monthly_data]
    totals = [row['total'] for row in monthly_data]

    sns.set(style="whitegrid")
    plt.figure(figsize=(9, 5))
    #sns.barplot(x=months, y=totals, palette="Blues_d")
    sns.barplot(x=months, y=totals, hue = months)

    plt.title('Monthly Spending')
    plt.xlabel('Month')
    plt.ylabel('Total Spent')

    # Save the plot to a temporary buffer.
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    # Encode the image to base64 so it can be embedded in the HTML.
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return img_str

# Monthly spending
@app.route('/monthly_spending')
def monthly_spending():
    chart = generate_monthly_spending_chart()

    conn = get_db_connection()
    months = conn.execute('''
    SELECT DISTINCT strftime('%Y-%m', date) AS month
    FROM expenses
    ORDER BY month DESC
    ''').fetchall()
    conn.close()

    return render_template('monthly_spending.html', chart=chart, months=months)

# View Monthly expenses
@app.route('/view_monthly_expenses')
def view_monthly_expenses():
    month = request.args.get('month')
    conn = get_db_connection()
    expenses = conn.execute('''
    SELECT expense_name, date, amount, c.name AS category, p.name AS payment_type, description
    FROM expenses e
    LEFT JOIN categories c ON e.category_id = c.id
    LEFT JOIN payment_types p ON e.payment_type_id = p.id
    WHERE strftime('%Y-%m', date) = ?
    ORDER BY date DESC
    ''', (month,)).fetchall()
    conn.close()

    return render_template('view_monthly_expenses.html', expenses=expenses, month=month)

# Search Expenses for Expense Name
@app.route('/search_expenses', methods=['GET'])
def search_expenses():
    query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT expense_name FROM expenses WHERE expense_name LIKE ?', (f'%{query}%',))
    expenses = cursor.fetchall()
    conn.close()
    return jsonify([expense['expense_name'] for expense in expenses])

if __name__ == '__main__':
    app.run(debug=True)
