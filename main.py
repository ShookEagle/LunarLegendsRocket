from sensors.bmp import Altimeter
from sensors.imu import IMU
from sensors.gps import BitBangGPS
from data.logger import FlightLogger

if __name__ == "__main__":
    alt = Altimeter()
    imu = IMU(0x68)
    gps = BitBangGPS(gpio_pin=17)

    logger = FlightLogger(imu=imu, bmp=alt)