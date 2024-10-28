import tkinter as tk
from tkinter import messagebox
import sqlite3
import threading
import datetime
import time

# --- Database Setup ---
def setup_database():
    conn = sqlite3.connect('pomodoro_tasks.db')
    c = conn.cursor()
    c.execute ('''CREATE TABLE IF NOT EXISTS tasks
                 (name text, time_spent integer, date text)''')
    conn.commit()
    conn.close()

setup_database()

# --- Functions for Database Operations ---
def add_task_to_db(task_name, time_spent):
    conn = sqlite3.connect('pomodoro_tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks VALUES (?,?,?)",
              (task_name, time_spent, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def retrieve_tasks():
    conn = sqlite3.connect('pomodoro_tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return rows

# --- Timer Functionality ---
class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.work_interval = 25  # Default in minutes
        self.break_interval = 5  # Default in minutes
        self.running = False
        self.time_left = self.work_interval * 60  # Convert minutes to seconds

        # GUI Elements
        self.task_name_label = tk.Label(master, text="Task Name:")
        self.task_name_label.pack()
        self.task_name_entry = tk.Entry(master, width=30)
        self.task_name_entry.pack()

        self.interval_frame = tk.Frame(master)
        self.interval_frame.pack()
        self.work_label = tk.Label(self.interval_frame, text="Work Interval (mins):")
        self.work_label.pack(side=tk.LEFT)
        self.work_entry = tk.Entry(self.interval_frame, width=5)
        self.work_entry.insert(0, str(self.work_interval))
        self.work_entry.pack(side=tk.LEFT)

        self.break_label = tk.Label(self.interval_frame, text="Break Interval (mins):")
        self.break_label.pack(side=tk.LEFT)
        self.break_entry = tk.Entry(self.interval_frame, width=5)
        self.break_entry.insert(0, str(self.break_interval))
        self.break_entry.pack(side=tk.LEFT)

        self.timer_label = tk.Label(master, text="25:00", font=('Helvetica', 48))
        self.timer_label.pack()

        self.control_frame = tk.Frame(master)
        self.control_frame.pack()
        self.start_button = tk.Button(self.control_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)

        self.tasks_button = tk.Button(master, text="View Tasks", command=self.view_tasks)
        self.tasks_button.pack()

    def countdown(self):
        if self.running:
            minutes, seconds = divmod(self.time_left, 60)
            self.timer_label.config(text=f"{minutes}:{seconds:02}")
            if self.time_left > 0:
                self.time_left -= 1
                self.master.after(1000, self.countdown)  # 1000ms = 1s
            else:
                if self.work_interval * 60 == self.time_left + 1:  # Just finished work interval
                    self.time_left = self.break_interval * 60
                    messagebox.showinfo("Break Time", "Take a break!")
                elif self.break_interval * 60 == self.time_left + 1:  # Just finished break interval
                    task_name = self.task_name_entry.get()
                    if task_name:
                        add_task_to_db(task_name, self.work_interval)
                        self.task_name_entry.delete(0, tk.END)
                    self.time_left = self.work_interval * 60
                    messagebox.showinfo("Work Time", "Back to work!")
                self.countdown()

    def start_timer(self):
        self.work_interval = int(self.work_entry.get())
        self.break_interval = int(self.break_entry.get())
        if not (3 <= self.work_interval <= 60 and 5 <= self.break_interval <= 15):
            messagebox.showerror("Invalid Intervals", "Work: 3-60 mins, Break: 5-15 mins")
            return
        self.time_left = self.work_interval * 60
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.countdown()

    def stop_timer(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def view_tasks(self):
        task_window = tk.Toplevel(self.master)
        task_window.title("Tasks")
        tasks = retrieve_tasks()
        task_text = tk.Text(task_window, width=80, height=20)
        task_text.pack()
        for task in tasks:
            task_text.insert(tk.END, f"Task: {task[0]}, Time Spent: {task[1]} minutes, Date: {task[2]}\n")
        task_text.config(state=tk.DISABLED)

# --- Main Application ---
root = tk.Tk()
root.title("Pomodoro Timer")
pomodoro = PomodoroTimer(root)
root.mainloop()