import tkinter as tk
from time import sleep
from progressbar import ProgressBar

# Default settings
work_time = 25  # minutes
break_time = 5  # minutes
long_break_time = 20  # minutes
cycles = 4
task_name = "Default Task"

# Initialize variables
current_time = work_time * 60
current_cycle = 1
is_running = False

# Initialize progress bar
progress_bar = ProgressBar()


def start_timer():
    global current_time, is_running

    if not is_running:
        is_running = True
        update_timer_label()
        progress_bar.start()
        while current_time > 0 and is_running:
            sleep(1)
            current_time -= 1
            update_timer_label()
            progress_bar.update(current_time / (work_time * 60))
        if current_cycle == cycles:
            play_sound("long_break.wav")
        else:
            play_sound("short_break.wav")


def stop_timer():
    global is_running

    is_running = False
    progress_bar.stop()


def reset_timer():
    global current_time, current_cycle, is_running

    current_time = work_time * 60
    current_cycle = 1
    is_running = False
    update_timer_label()
    progress_bar.reset()


def update_timer_label():
    minutes, seconds = divmod(current_time, 60)
    timer_label.config(text=f"{minutes:02}:{seconds:02}")


def play_sound(sound_file):
    # Implement sound playing using your preferred library
    # (e.g., playsound)
    pass


# Create the main window
window = tk.Tk()
window.title("Pomodoro Timer")
window.geometry("300x250")

# Create labels
task_label = tk.Label(window, text=f"Task: {task_name}")
timer_label = tk.Label(window, text="25:00", font=("Arial", 32))
cycle_label = tk.Label(window, text=f"Cycle: {current_cycle}/{cycles}")

# Create buttons
start_button = tk.Button(window, text="Start", command=start_timer)
stop_button = tk.Button(window, text="Stop", command=stop_timer)
reset_button = tk.Button(window, text="Reset", command=reset_timer)

# Create progress bar
progress_bar = ProgressBar(window, orientation="horizontal")

# Layout widgets
task_label.pack(pady=(10, 0))
timer_label.pack(pady=(10, 0))
cycle_label.pack(pady=(10, 0))
progress_bar.pack(pady=(10, 0))

start_button.pack(side="left", padx=(20, 10))
stop_button.pack(side="left", padx=(10, 10))
reset_button.pack(side="left", padx=(10, 20))

# Run the main loop
window.mainloop()
