import time
from datetime import datetime

import math
import pandas as pd
from pynput.mouse import Listener as MouseListener

# Parameters
LOG_INTERVAL_SECONDS = 5  # How often to log mouse position
log_file_path = "mouse_activity_log.csv"

# Initialize variables
current_mouse_position = (0, 0)
last_activity_time = None
total_mouse_movement_since_last_log = 0


def open_log_file():
    """Opens the log file and creates headers if it's new."""
    try:
        df = pd.read_csv(log_file_path)
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=["timestamp", "x_position", "y_position", "distance_moved", "idle_time"]
        )
        df.to_csv(log_file_path, index=False)


def on_mouse_move(x, y):
    """Triggered when the mouse moves.
    Updates the current mouse position and calculates the distance moved since the last log.
    """
    global current_mouse_position, last_activity_time, total_mouse_movement_since_last_log

    if current_mouse_position:
        distance = math.sqrt((x - current_mouse_position[0]) ** 2 + (y - current_mouse_position[1]) ** 2)
        total_mouse_movement_since_last_log += distance

    current_mouse_position = (x, y)


def log_activity():
    """Logs the current mouse activity to the CSV file.
    Logs timestamp, position, distance moved, and idle time.
    """
    global current_mouse_position, last_activity_time, total_mouse_movement_since_last_log

    now = datetime.now()
    idle_time = (now - last_activity_time).total_seconds() if last_activity_time else 0
    df = pd.DataFrame(
        [[now, current_mouse_position[0], current_mouse_position[1], total_mouse_movement_since_last_log, idle_time]],
        columns=["timestamp", "x_position", "y_position", "distance_moved", "idle_time"],
    )
    df.to_csv(log_file_path, mode="a", header=False, index=False)
    last_activity_time = now
    total_mouse_movement_since_last_log = 0  # Reset distance moved after logging


def monitor_mouse():
    """Starts the mouse listener and logs activity continuously."""
    listener = MouseListener(on_move=on_mouse_move)
    listener.start()
    open_log_file()  # Open the log file before starting logging

    try:
        while True:
            log_activity()
            time.sleep(LOG_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        listener.stop()


if __name__ == "__main__":
    monitor_mouse()
