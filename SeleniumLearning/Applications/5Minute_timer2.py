import tkinter as tk
import threading
import time
import winsound  # For Windows (use pygame for cross-platform)
from datetime import datetime, time

end_seconds = 0


def start_timer():
    # Get the user input for start and end times
    start_time = start_entry.get()
    end_time = end_entry.get()

    # Convert start and end times to seconds since midnight
    start_seconds = sum(int(x) * 60**i for i, x in enumerate(reversed(start_time.split(":"))))
    end_seconds = sum(int(x) * 60**i for i, x in enumerate(reversed(end_time.split(":"))))

    def repeat_timer():
        current_time = datetime.now().time().strftime("%H:%M:%S")
        current_seconds = sum(int(x) * 60**i for i, x in enumerate(reversed(current_time.split(":"))))
        print(f"Current Time is {current_time} : {current_seconds}")

        if start_seconds <= current_seconds < end_seconds:
            print(f"Timer: {current_time}")
            # Play a sound (adjust the path to your sound file)
            winsound.PlaySound("C://windows//media//Alarm05.wav", winsound.SND_FILENAME)

        # Repeat every 5 minutes
        threading.Timer(300, repeat_timer).start()

    repeat_timer()

# Create the GUI
root = tk.Tk()
root.title("Repeating Timer")

start_label = tk.Label(root, text="Start Time (HH:MM):")
start_entry = tk.Entry(root)
end_label = tk.Label(root, text="End Time (HH:MM):")
end_entry = tk.Entry(root)
start_button = tk.Button(root, text="Start Timer", command=start_timer)

remaining_label = tk.Label(root, text="Remaining Time:")
remaining_var = tk.StringVar()
remaining_time_label = tk.Label(root, textvariable=remaining_var)

def update_remaining_time():
    current_time = datetime.now().time().strftime("%H:%M:%S")
    current_seconds = sum(int(x) * 60**i for i, x in enumerate(reversed(current_time.split(":"))))
    remaining_seconds = end_seconds - current_seconds

    if remaining_seconds > 0:
        remaining_minutes, remaining_secs = divmod(int(remaining_seconds), 60)
        remaining_var.set(f"{remaining_minutes:02d}:{remaining_secs:02d}")
        root.after(1000, update_remaining_time)  # Update every second
    else:
        remaining_var.set("00:00")  # Timer expired

update_remaining_time()

start_label.pack()
start_entry.pack()
end_label.pack()
end_entry.pack()
start_button.pack()
remaining_label.pack()
remaining_time_label.pack()

root.mainloop()
