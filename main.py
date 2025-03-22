# main.py

import csv
import time
from datetime import datetime
from utils.localizer import localizer
from components.camera_dual import DualCamera

# Placeholder sensor classes
class BMP388: pass
class GPS: pass
class MPU6050: pass
class SIM800L: pass

# Placeholder launch detection
def detect_launch(altitude, accel_z, threshold_alt=2.0, threshold_accel=3.0):
    return altitude > threshold_alt and abs(accel_z) > threshold_accel

# ====== Logging Setup ======
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = f"data/flight_{timestamp}.csv"
with open(log_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "altitude", "temperature", "latitude", "longitude",
                     "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"])

# ====== System Startup ======
localizer.print_local("startup")

# ====== Initialize Components ======
bmp = BMP388()         # TODO: Implement
gps = GPS()            # TODO: Implement
imu = MPU6050()        # TODO: Implement
sim = SIM800L()        # TODO: Implement
cameras = DualCamera()
cameras.start_prebuffering()

localizer.print_local("waiting_for_launch")

# ====== Flight Loop ======
launch_detected = False

try:
    while True:
        timestamp = time.time()

        # Replace with real sensor reads
        altitude = 0.0
        temperature = 0.0
        latitude = 0.0
        longitude = 0.0
        accel = (0.0, 0.0, 4.5)  # Simulated spike for testing
        gyro = (0.0, 0.0, 0.0)

        # Detect Launch
        if not launch_detected and detect_launch(altitude, accel[2]):
            launch_detected = True
            localizer.print_local("launch_detected")
            cameras.start_recording()

        # Log Data
        with open(log_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, altitude, temperature, latitude, longitude,
                *accel, *gyro
            ])

        time.sleep(0.5)

except KeyboardInterrupt:
    localizer.print_local_error("shutdown")
    cameras.stop_recording()
