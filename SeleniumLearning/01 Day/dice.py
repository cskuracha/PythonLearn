import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def roll_dice():
    return random.randint(1, 6)

def update(frame):
    ax.clear()
    result = roll_dice()
    ax.text(0.5, 0.5, f"Rolling... {result}", ha='center', va='center', fontsize=20)

fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, frames=range(10), repeat=False, blit=False, interval=500)

plt.show()