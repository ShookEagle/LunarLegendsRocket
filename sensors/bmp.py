import board
import adafruit_bmp3xx


class Altimeter:
    def __init__(self):
        i2c = board.I2C()
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
        self.bmp.sea_level_pressure = 1011.2234915017

    def read_altitude(self):
        return self.bmp.altitude

    def read_bmp_temperature(self):
        return self.bmp.temperature

    def read_pressure(self):
        return self.bmp.pressure