import mpu6050

class IMU:
    def __init__(self, address):
        self.address = address
        self.mpu = mpu6050.mpu6050(address)

    def read_acceleration(self):
        return self.mpu.get_accel_data()

    def read_gyro(self):
        return self.mpu.get_gyro_data().get("x")

    def read_imu_temp(self):
        return self.mpu.get_temp()