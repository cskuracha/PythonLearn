# main.py

from tkinter import Tk
from database import create_db
from ui import PomodoroTimerUI


def main():
    # Initialize the database
    create_db()

    # Set up the UI
    root = Tk()
    app = PomodoroTimerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
