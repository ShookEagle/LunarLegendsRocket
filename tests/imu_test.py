import sys
import os
import time

from sensors.imu import Altimeter

# Initialize the IMU
imu = Altimeter()


try:
    while True:
        accel = imu.read_accel()
        gyro = imu.read_gyro()
        temperature = imu.read_imu_temperature()

        print(f"[Accel] x={accel[0]:.2f} m/s², y={accel[1]:.2f} m/s², z={accel[2]:.2f} m/s²")
        print(f"[Gyro]  x={gyro[0]:.2f} °/s, y={gyro[1]:.2f} °/s, z={gyro[2]:.2f} °/s")
        print (f"[Temperature] {temperature} deg C")
        print("-------------------------------------------------------------")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[IMU Test] Stopped by user.")
