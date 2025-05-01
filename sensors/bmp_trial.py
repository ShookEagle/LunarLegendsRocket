import adafruit_bus_device.i2c_device as i2c_device
import board
from busio import I2C
import adafruit_bmp3xx


class BMP:
    def __init__(self):
        i2c = i2c_device.I2CDevice(I2C(board.SCL, board.SDA), device_address=77)
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

    def read(self):
        return self.bmp.altitude