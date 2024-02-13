import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime, timedelta


class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("5-Minute Repeating Timer")

        self.label = tk.Label(master, text="Timer: 00:00")
        self.label.pack()

        self.remaining_label = tk.Label(master, text="")
        self.remaining_label.pack()

        self.start_button = tk.Button(master, text="Start Timer", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Timer", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack()

        self.entry_frame = tk.Frame(master)
        self.entry_frame.pack()

        self.start_label = tk.Label(self.entry_frame, text="Start Time (HH:MM): ")
        self.start_label.grid(row=0, column=0)
        self.start_entry = tk.Entry(self.entry_frame)
        self.start_entry.grid(row=0, column=1)

        self.end_label = tk.Label(self.entry_frame, text="End Time (HH:MM): ")
        self.end_label.grid(row=1, column=0)
        self.end_entry = tk.Entry(self.entry_frame)
        self.end_entry.grid(row=1, column=1)

        self.current_time = None
        self.is_running = False

    def start_timer(self):
        start_time = self.start_entry.get()
        end_time = self.end_entry.get()

        if not self.validate_time(start_time) or not self.validate_time(end_time):
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM format.")
            return

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.is_running = True
        self.update_timer()

    def stop_timer(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_timer(self):
        while self.is_running:
            current_time = datetime.now().strftime("%H:%M")
            self.label.config(text="Timer: " + current_time)

            if self.start_entry.get() <= current_time <= self.end_entry.get():
                end_of_interval = datetime.now() + timedelta(minutes=5)
                remaining_time = end_of_interval - datetime.now()
                self.remaining_label.config(text=f"Next Interval in: {remaining_time.seconds // 60} minutes")

            time.sleep(1)  # Check every second

    @staticmethod
    def validate_time(time_str):
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False


root = tk.Tk()
app = TimerApp(root)
root.mainloop()
