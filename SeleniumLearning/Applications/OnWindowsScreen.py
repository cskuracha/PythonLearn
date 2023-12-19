import pyautogui
import time

# The time we want to wait (in seconds) between each step
wait_time = 0.1

# The points that make up the path of our drawing
points = [(100, 100), (200, 200), (100, 200), (200, 100)]

# Move the mouse to the start of the path
pyautogui.moveTo(points[0][0], points[0][1])
time.sleep(wait_time)

# Click and hold the left mouse button
pyautogui.mouseDown(button='left')

# Move the mouse along the path
for point in points[1:]:
    pyautogui.moveTo(point[0], point[1])
    time.sleep(wait_time)

# Release the mouse button
pyautogui.mouseUp(button='left')
