# ui.py

import tkinter as tk
from tkinter import messagebox, ttk
import time
import threading
from database import add_task, get_tasks, delete_task

class PomodoroTimerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x500")

        # Timer variables
        self.is_running = False
        self.work_time = 25 * 60  # default work time in seconds
        self.break_time = 5 * 60  # default break time in seconds
        self.remaining_time = self.work_time

        # Task variables
        self.current_task = None
        self.time_spent = 0

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Timer display
        self.label_timer = tk.Label(self.root, text="25:00", font=("Helvetica", 48))
        self.label_timer.pack(pady=20)

        # Start, Reset, and Break buttons
        self.button_start = tk.Button(self.root, text="Start Work", command=self.start_work)
        self.button_start.pack(side=tk.LEFT, padx=20)

        self.button_break = tk.Button(self.root, text="Take Break", command=self.start_break, state=tk.DISABLED)
        self.button_break.pack(side=tk.LEFT, padx=20)

        self.button_reset = tk.Button(self.root, text="Reset", command=self.reset_timer)
        self.button_reset.pack(side=tk.LEFT, padx=20)

        # Task management
        self.label_task = tk.Label(self.root, text="Tasks", font=("Helvetica", 14))
        self.label_task.pack(pady=10)

        self.entry_task = tk.Entry(self.root, width=30)
        self.entry_task.pack(pady=5)
        self.button_add_task = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.button_add_task.pack(pady=5)

        self.tree_tasks = ttk.Treeview(self.root, columns=("Name", "Time", "Date"), show="headings")
        self.tree_tasks.heading("Name", text="Task Name")
        self.tree_tasks.heading("Time", text="Time Spent (min)")
        self.tree_tasks.heading("Date", text="Date Added")
        self.tree_tasks.pack(fill=tk.BOTH, expand=True, pady=10)
        self.populate_tasks()

        # Timer updates
        self.update_timer_display()

    def start_work(self):
        if not self.is_running:
            self.is_running = True
            self.remaining_time = self.work_time
            self.button_start.config(state=tk.DISABLED)
            self.button_break.config(state=tk.NORMAL)
            threading.Thread(target=self.run_timer).start()

    def start_break(self):
        if not self.is_running:
            self.is_running = True
            self.remaining_time = self.break_time
            self.button_start.config(state=tk.NORMAL)
            self.button_break.config(state=tk.DISABLED)
            threading.Thread(target=self.run_timer).start()

    def reset_timer(self):
        self.is_running = False
        self.remaining_time = self.work_time
        self.update_timer_display()
        self.button_start.config(state=tk.NORMAL)
        self.button_break.config(state=tk.DISABLED)

    def run_timer(self):
        while self.remaining_time > 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.label_timer.config(text=f"{mins:02}:{secs:02}")
            time.sleep(1)
            self.remaining_time -= 1

        if self.remaining_time == 0:
            self.is_running = False
            self.time_spent += self.work_time // 60
            self.update_task_time()
            messagebox.showinfo("Pomodoro Timer", "Time's up! Take a break or start another session.")
            self.reset_timer()

    def add_task(self):
        task_name = self.entry_task.get().strip()
        if task_name:
            add_task(task_name, 0)  # initial time spent = 0
            self.entry_task.delete(0, tk.END)
            self.populate_tasks()

    def populate_tasks(self):
        for i in self.tree_tasks.get_children():
            self.tree_tasks.delete(i)
        tasks = get_tasks()
        for task in tasks:
            self.tree_tasks.insert("", "end", values=(task[1], task[2], task[3]))

    def update_task_time(self):
        if self.current_task:
            add_task(self.current_task, self.time_spent)
            self.populate_tasks()

    def update_timer_display(self):
        mins, secs = divmod(self.remaining_time, 60)
        self.label_timer.config(text=f"{mins:02}:{secs:02}")
        self.root.after(1000, self.update_timer_display)
