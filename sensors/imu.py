import board
import adafruit_mpu6050


class Altimeter:
    def __init__(self):
        i2c = board.I2C()
        self.imu = adafruit_mpu6050.MPU6050(i2c)

    def read_gyro(self):
        return self.imu.gyro

    def read_inu_temperature(self):
        return self.imu.temperature

    def read_accel(self):
        return self.imu.acceleration