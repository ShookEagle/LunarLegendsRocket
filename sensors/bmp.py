import adafruit_bmp3xx
import busio
from adafruit_blinka import board

class Altimeter:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)  # this works on Raspberry Pi with Adafruit library
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

    def read_altitude(self):
        return self.bmp.altitude

    def read_pressure(self):
        return self.bmp.pressure

    def read_bmp_temp(self):
        return self.bmp.temperature