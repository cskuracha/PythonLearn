import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import time
import threading
from plyer import notification
import json
import os


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('pomodoro.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_time INTEGER DEFAULT 0,
                    completed BOOLEAN DEFAULT 0
                )
            ''')

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER,
                    start_time TIMESTAMP,
                    duration INTEGER,
                    type TEXT,
                    FOREIGN KEY (task_id) REFERENCES tasks (id)
                )
            ''')

    def add_task(self, task_name):
        with self.conn:
            cursor = self.conn.execute(
                'INSERT INTO tasks (name) VALUES (?)',
                (task_name,)
            )
            return cursor.lastrowid

    def update_task(self, task_id, time_spent):
        with self.conn:
            self.conn.execute(
                'UPDATE tasks SET total_time = total_time + ? WHERE id = ?',
                (time_spent, task_id)
            )

    def get_tasks(self):
        cursor = self.conn.execute('SELECT id, name, total_time FROM tasks WHERE completed = 0')
        return cursor.fetchall()

    def log_session(self, task_id, duration, session_type):
        with self.conn:
            self.conn.execute(
                'INSERT INTO sessions (task_id, start_time, duration, type) VALUES (?, ?, ?, ?)',
                (task_id, datetime.now(), duration, session_type)
            )

    def get_statistics(self):
        cursor = self.conn.execute('''
            SELECT 
                COUNT(*) as total_sessions,
                SUM(duration) as total_time,
                AVG(duration) as avg_session_length
            FROM sessions
            WHERE type = 'work'
        ''')
        return cursor.fetchone()


class Settings:
    def __init__(self):
        self.default_settings = {
            'work_duration': 25,
            'break_duration': 5,
            'theme': 'light',
            'notifications': True
        }
        self.load_settings()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = self.default_settings
            self.save_settings()

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)

    def get(self, key):
        return self.settings.get(key, self.default_settings[key])

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("600x400")

        self.db = Database()
        self.settings = Settings()

        self.current_task = None
        self.timer_running = False
        self.remaining_time = 0
        self.timer_thread = None

        self.setup_ui()
        self.load_tasks()
        self.apply_theme()

    def setup_ui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Timer display
        self.time_label = ttk.Label(
            self.main_frame,
            text="25:00",
            font=("Arial", 48)
        )
        self.time_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Task section
        task_frame = ttk.LabelFrame(self.main_frame, text="Tasks", padding="5")
        task_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Task list
        self.task_listbox = tk.Listbox(task_frame, height=6)
        self.task_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Add task entry
        self.task_entry = ttk.Entry(task_frame)
        self.task_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(
            task_frame,
            text="Add Task",
            command=self.add_task
        ).grid(row=1, column=1, padx=5)

        # Control buttons
        control_frame = ttk.Frame(self.main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(
            control_frame,
            text="Start",
            command=self.start_timer
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            control_frame,
            text="Stop",
            command=self.stop_timer
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            control_frame,
            text="Reset",
            command=self.reset_timer
        ).grid(row=0, column=2, padx=5)

        # Settings button
        ttk.Button(
            self.main_frame,
            text="Settings",
            command=self.show_settings
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # Statistics button
        ttk.Button(
            self.main_frame,
            text="Statistics",
            command=self.show_statistics
        ).grid(row=4, column=0, columnspan=2)

    def apply_theme(self):
        style = ttk.Style()
        if self.settings.get('theme') == 'dark':
            self.root.configure(bg='#2d2d2d')
            style.configure('TFrame', background='#2d2d2d')
            style.configure('TLabel', background='#2d2d2d', foreground='white')
            style.configure('TButton', background='#444444', foreground='white')
        else:
            self.root.configure(bg='white')
            style.configure('TFrame', background='white')
            style.configure('TLabel', background='white', foreground='black')
            style.configure('TButton', background='#f0f0f0')

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.db.get_tasks()
        for task_id, name, total_time in tasks:
            self.task_listbox.insert(tk.END, f"{name} ({total_time} min)")

    def add_task(self):
        task_name = self.task_entry.get().strip()
        if task_name:
            self.db.add_task(task_name)
            self.task_entry.delete(0, tk.END)
            self.load_tasks()

    def start_timer(self):
        if not self.timer_running:
            selected = self.task_listbox.curselection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a task first!")
                return

            self.current_task = selected[0]
            self.timer_running = True
            self.remaining_time = self.settings.get('work_duration') * 60

            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def stop_timer(self):
        self.timer_running = False
        if self.timer_thread:
            self.timer_thread.join()

    def reset_timer(self):
        self.stop_timer()
        self.remaining_time = self.settings.get('work_duration') * 60
        self.update_timer_display()

    def run_timer(self):
        start_time = time.time()
        while self.timer_running and self.remaining_time > 0:
            self.remaining_time = max(0, self.remaining_time - 1)
            self.update_timer_display()
            time.sleep(1)

        if self.remaining_time == 0:
            self.timer_running = False
            self.show_notification("Time's up!", "Work session completed!")
            self.db.update_task(self.current_task, self.settings.get('work_duration'))
            self.load_tasks()

    def update_timer_display(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_label.configure(text=f"{minutes:02d}:{seconds:02d}")

    def show_notification(self, title, message):
        if self.settings.get('notifications'):
            notification.notify(
                title=title,
                message=message,
                app_icon=None,
                timeout=10,
            )

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x200")

        ttk.Label(settings_window, text="Work Duration (minutes):").pack()
        work_duration = ttk.Entry(settings_window)
        work_duration.insert(0, str(self.settings.get('work_duration')))
        work_duration.pack()

        ttk.Label(settings_window, text="Break Duration (minutes):").pack()
        break_duration = ttk.Entry(settings_window)
        break_duration.insert(0, str(self.settings.get('break_duration')))
        break_duration.pack()

        theme_var = tk.StringVar(value=self.settings.get('theme'))
        ttk.Radiobutton(
            settings_window,
            text="Light Theme",
            variable=theme_var,
            value="light"
        ).pack()
        ttk.Radiobutton(
            settings_window,
            text="Dark Theme",
            variable=theme_var,
            value="dark"
        ).pack()

        notifications_var = tk.BooleanVar(value=self.settings.get('notifications'))
        ttk.Checkbutton(
            settings_window,
            text="Enable Notifications",
            variable=notifications_var
        ).pack()

        def save_settings():
            self.settings.set('work_duration', int(work_duration.get()))
            self.settings.set('break_duration', int(break_duration.get()))
            self.settings.set('theme', theme_var.get())
            self.settings.set('notifications', notifications_var.get())
            self.apply_theme()
            settings_window.destroy()

        ttk.Button(
            settings_window,
            text="Save",
            command=save_settings
        ).pack(pady=10)

    def show_statistics(self):
        stats = self.db.get_statistics()
        if stats:
            total_sessions, total_time, avg_session = stats
            messagebox.showinfo(
                "Statistics",
                f"Total Sessions: {total_sessions}\n"
                f"Total Time: {total_time} minutes\n"
                f"Average Session Length: {avg_session:.1f} minutes"
            )


def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()