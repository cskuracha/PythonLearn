# database.py

import sqlite3
from datetime import datetime

def create_db():
    conn = sqlite3.connect("pomodoro.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        time_spent INTEGER,
                        date TEXT
                    )''')
    conn.commit()
    conn.close()

def add_task(name, time_spent):
    conn = sqlite3.connect("pomodoro.db")
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO tasks (name, time_spent, date) VALUES (?, ?, ?)", (name, time_spent, date))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect("pomodoro.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect("pomodoro.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
