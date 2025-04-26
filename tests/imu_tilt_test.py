import sys
import os
import time

from sensors.imu import IMU

def interpret_tilt(angle):
    """
    Classify tilt based on angle
    """
    if angle < 15:
        return "UPRIGHT"
    elif 75 <= angle <= 105:
        return "SIDEWAYS"
    elif angle > 165:
        return "UPSIDE DOWN"
    else:
        return "TILTED"

def main():
    imu = IMU(0x68)

    print("\n[IMU Tilt Test] Starting... (Press Ctrl+C to stop)\n")

    try:
        while True:
            tilt_angle = imu.calculate_tilt()
            tilt_status = interpret_tilt(tilt_angle)
            gyro_read = imu.read_gyro()
            accel_read = imu.read_acceleration()
            temp_read = imu.read_imu_temp()
            total_accel = (accel_read["x"] ** 2 + accel_read["y"] ** 2 + accel_read["z"] ** 2) ** 0.5

            print(f"[Tilt] {tilt_angle:.1f}° - Status: {tilt_status}")
            print(f"Gyro:{gyro_read}")
            print(f"Accel:{accel_read}")
            print(f"Accel Vec Magnitude :{total_accel}")
            print(f"Temp: {temp_read}")
            print("-------------------------------------------------------------")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[IMU Tilt Test] Stopped by user.")

if __name__ == "__main__":
    main()
