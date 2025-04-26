import sys
import os
import time

from sensors.imu import IMU

# Initialize the IMU
imu = IMU(0x68)

print("\n[IMU Test] Starting data readout... (Press Ctrl+C to stop)")

try:
    while True:
        accel = imu.read_acceleration()
        gyro = imu.read_gyro()

        print(f"[Accel] x={accel['x']:.2f} m/s², y={accel['y']:.2f} m/s², z={accel['z']:.2f} m/s²")
        print(f"[Gyro]  x={gyro['x']:.2f} °/s, y={gyro['y']:.2f} °/s, z={gyro['z']:.2f} °/s")
        print("-------------------------------------------------------------")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[IMU Test] Stopped by user.")
