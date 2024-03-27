import csv
from datetime import datetime, timedelta

# Define the start and end times
start_time = datetime(2023, 3, 27, 8, 0, 0)  # YYYY, MM, DD, HH, MM, SS
end_time = datetime(2023, 3, 27, 19, 0, 0)

# Define the time interval (5 minutes)
interval = timedelta(minutes=5)

# Create a list to store the time blocks
time_blocks = []

# Loop through the time range and create the time blocks
current_time = start_time
while current_time < end_time:
    time_blocks.append(current_time.strftime("%H:%M:%S"))
    current_time += interval

# Export the time blocks to a CSV file
with open("time_blocks.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Time Block"])  # Write the header row
    for block in time_blocks:
        writer.writerow([block])