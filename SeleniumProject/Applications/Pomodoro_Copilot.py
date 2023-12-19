import tkinter as tk
from tkinter import messagebox, ttk
import time
import threading

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.geometry("300x200")
        self.master.configure(bg='light blue')

        self.task_name_label = tk.Label(master, text="Task Name", bg='light blue')
        self.task_name_label.grid(row=0, column=0)

        self.task_name_entry = tk.Entry(master)
        self.task_name_entry.grid(row=0, column=1)

        self.time_label = tk.Label(master, text="Time (in minutes)", bg='light blue')
        self.time_label.grid(row=1, column=0)

        self.time_var = tk.StringVar()
        self.time_dropdown = ttk.Combobox(master, textvariable=self.time_var)
        self.time_dropdown['values'] = list(range(5, 65, 5))
        self.time_dropdown.grid(row=1, column=1)

        self.progress = ttk.Progressbar(master, orient='horizontal', length=200, mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=2)

        self.start_button = tk.Button(master, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=3, column=0)

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_timer, state='disabled')
        self.pause_button.grid(row=3, column=1)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer, state='disabled')
        self.stop_button.grid(row=4, column=0)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer, state='disabled')
        self.reset_button.grid(row=4, column=1)

        self.timer_active = False
        self.timer_paused = False

    def start_timer_thread(self):
        self.timer_thread = threading.Thread(target=self.start_timer)
        self.timer_thread.start()

    def start_timer(self):
        if not self.timer_active:
            self.timer_active = True
            self.pause_button['state'] = 'normal'
            self.stop_button['state'] = 'normal'
            self.reset_button['state'] = 'normal'
            self._run_timer()

    def pause_timer(self):
        self.timer_paused = not self.timer_paused
        self.pause_button['text'] = "Resume" if self.timer_paused else "Pause"

    def stop_timer(self):
        self.timer_active = False
        self.timer_paused = False
        self.pause_button['state'] = 'disabled'
        self.stop_button['state'] = 'disabled'
        self.reset_button['state'] = 'disabled'
        self.progress['value'] = 0

    def reset_timer(self):
        self.timer_active = False
        self.timer_paused = False
        self.pause_button['state'] = 'disabled'
        self.stop_button['state'] = 'disabled'
        self.reset_button['state'] = 'disabled'
        self.progress['value'] = 0

    def _run_timer(self):
        task_name = self.task_name_entry.get()
        minutes = int(self.time_var.get())

        if not 5 <= minutes <= 60:
            messagebox.showerror("Error", "Please enter a time between 5 and 60 minutes.")
            return

        print(f"Starting task: {task_name}")
        self.progress['maximum'] = minutes * 60
        for i in range(minutes*60, -1, -1):
            if not self.timer_active:
                break
            while self.timer_paused:
                time.sleep(1)
            mins, secs = divmod(i, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            print(time_format, end='\r')
            self.progress['value'] = minutes * 60 - i
            self.master.update_idletasks()
            time.sleep(1)

        if self.timer_active:
            self.progress['value'] = 0
            messagebox.showinfo("Task Completed", f"Task {task_name} completed!")
            self.timer_active = False

root = tk.Tk()
my_timer = PomodoroTimer(root)
root.mainloop()
