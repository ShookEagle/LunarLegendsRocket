import json
import math
import time

import mpu6050

class IMU:
    def __init__(self, address):
        self.address = address
        self.mpu = mpu6050.mpu6050(address)

        self.attitude_corrector = AttitudeCorrector()
        self.gyro_bias = {'x': 0, 'y': 0, 'z': 0}

        self.calibrate_imu()

    def calibrate_imu(self, samples=100):
        accel_sum = {'x': 0, 'y': 0, 'z': 0}
        gyro_sum = {'x': 0, 'y': 0, 'z': 0}

        print("[IMU] Calibrating... Please keep rocket still.")

        for _ in range(samples):
            accel = self.mpu.get_accel_data()
            gyro = self.mpu.get_gyro_data()

            for axis in ['x', 'y', 'z']:
                accel_sum[axis] += accel[axis]
                gyro_sum[axis] += gyro[axis]

            time.sleep(0.01)

        # Average
        accel_avg = {k: v / samples for k, v in accel_sum.items()}
        gyro_avg = {k: v / samples for k, v in gyro_sum.items()}

        self.attitude_corrector.calibrate(accel_avg)
        self.gyro_bias = gyro_avg

        print("[IMU] Calibration complete.")

    def read_acceleration(self):
        raw = self.mpu.get_accel_data()
        rotated = self.attitude_corrector.apply(raw)
        return rotated

    def read_gyro(self):
        raw = self.mpu.get_gyro_data()
        corrected = {
            axis: raw[axis] - self.gyro_bias[axis] for axis in ['x', 'y', 'z']
        }
        return corrected

    def read_imu_temp(self):
        return self.mpu.get_temp()


class AttitudeCorrector:
    def __init__(self):
        self.rotation_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # Identity until calibrated

    def calibrate(self, measured_gravity):
        # Target vector (what we want gravity to point to)
        target = [0.0, 9.8, 0.0]  # Because Y axis is vertical!

        # Normalize both vectors
        g = self._normalize([
            measured_gravity['x'],
            measured_gravity['y'],
            measured_gravity['z']
        ])
        t = self._normalize(target)

        # Calculate rotation axis (cross product)
        axis = [
            g[1] * t[2] - g[2] * t[1],
            g[2] * t[0] - g[0] * t[2],
            g[0] * t[1] - g[1] * t[0]
        ]

        axis_norm = math.sqrt(sum(a ** 2 for a in axis))
        if axis_norm == 0:
            self.rotation_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # No rotation needed
            return

        axis = [a / axis_norm for a in axis]

        # Calculate rotation angle (dot product then arccos)
        dot = sum(g[i] * t[i] for i in range(3))
        angle = math.acos(dot)

        self.rotation_matrix = self._rotation_matrix(axis, angle)

    def apply(self, vector):
        # Apply rotation matrix to vector
        return {
            'x': sum(self.rotation_matrix[0][i] * vector[axis] for i, axis in enumerate(['x', 'y', 'z'])),
            'y': sum(self.rotation_matrix[1][i] * vector[axis] for i, axis in enumerate(['x', 'y', 'z'])),
            'z': sum(self.rotation_matrix[2][i] * vector[axis] for i, axis in enumerate(['x', 'y', 'z'])),
        }

    def _normalize(self, v):
        norm = math.sqrt(sum(x ** 2 for x in v))
        return [x / norm for x in v]

    def _rotation_matrix(self, axis, theta):
        # Rodrigues' rotation formula
        a = math.cos(theta)
        b = math.sin(theta)
        x, y, z = axis
        return [
            [a + (1 - a) * x * x, (1 - a) * x * y - b * z, (1 - a) * x * z + b * y],
            [(1 - a) * y * x + b * z, a + (1 - a) * y * y, (1 - a) * y * z - b * x],
            [(1 - a) * z * x - b * y, (1 - a) * z * y + b * x, a + (1 - a) * z * z]
        ]