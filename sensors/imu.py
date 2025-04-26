import mpu6050
import time
import math

class IMU:
    def __init__(self, address):
        self.address = address
        self.mpu = mpu6050.mpu6050(address)

        self.gyro_bias = {'x': 0, 'y': 0, 'z': 0}
        self.calibrate_gyro()

    def calibrate_gyro(self, samples=100):
        """
        Calibrates gyroscope biases while stationary.
        """
        print("[IMU] Calibrating gyroscope bias... Please keep rocket still.")
        gyro_sum = {'x': 0, 'y': 0, 'z': 0}

        for _ in range(samples):
            gyro = self.mpu.get_gyro_data()
            for axis in ['x', 'y', 'z']:
                gyro_sum[axis] += gyro[axis]
            time.sleep(0.01)

        self.gyro_bias = {k: v / samples for k, v in gyro_sum.items()}
        print(f"[IMU] Gyro bias: {self.gyro_bias}")

    def read_acceleration(self):
        """
        Returns raw acceleration dict: x, y, z in m/s²
        """
        return self.mpu.get_accel_data()

    def read_gyro(self):
        """
        Returns bias-corrected gyro dict: x, y, z in degrees/sec
        """
        raw = self.mpu.get_gyro_data()
        corrected = {
            axis: raw[axis] - self.gyro_bias[axis]
            for axis in ['x', 'y', 'z']
        }
        return corrected

    def read_imu_temp(self):
        """
        Returns temperature in °C
        """
        return self.mpu.get_temp()

    def calculate_tilt(self, accel=None):
        """
        Calculates tilt angle from current accelerometer reading.
        Returns tilt angle in degrees relative to +Y axis (up).
        """
        if accel is None:
            accel = self.read_acceleration()

        # Define your "up" vector: positive Y axis
        up_vector = [0.0, 9.8, 0.0]
        measured_vector = [accel['x'], accel['y'], accel['z']]

        # Normalize vectors
        up_norm = math.sqrt(sum(u**2 for u in up_vector))
        measured_norm = math.sqrt(sum(m**2 for m in measured_vector))

        if measured_norm == 0:
            return 0.0

        # Dot product
        dot = sum(measured_vector[i] * up_vector[i] for i in range(3))

        # Angle in radians → degrees
        angle_rad = math.acos(dot / (measured_norm * up_norm))
        angle_deg = math.degrees(angle_rad)

        return angle_deg
