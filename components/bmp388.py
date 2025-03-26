import time
import board
import adafruit_bmp3xx


class BMP388:
    def __init__(self):
        # Initialize I2C bus
        i2c = board.I2C()
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

        # Set oversampling settings
        self.bmp.pressure_oversampling = 8
        self.bmp.temperature_oversampling = 2

    def get_temperature(self):
        """Returns the temperature in degrees Celsius."""
        return self.bmp.temperature

    def get_pressure(self):
        """Returns the pressure in hPa."""
        return self.bmp.pressure

    def get_altitude(self, sea_level_pressure=1013.25):
        """Calculates and returns the altitude in meters.

        Args:
            sea_level_pressure (float): The local sea level pressure in hPa.

        Returns:
            float: Altitude in meters.
        """
        self.bmp.sea_level_pressure = sea_level_pressure
        return self.bmp.altitude
