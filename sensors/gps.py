import serial
import pynmea2

class GPS:
    def __init__(self):
        self.ser = serial.Serial(port="/dev/ttyAMA3", baudrate=9600, timeout=1)

    def read(self):
        while True:
            line = self.ser.readline().decode('ascii', errors='replace').strip()
            if line.startswith('$GPGGA'):
                try:
                    msg = pynmea2.parse(line)
                    lat = msg.latitude
                    lon = msg.longitude
                    if lat and lon:
                        return (lat, lon)
                except pynmea2.ParseError:
                    continue

    def close(self):
        self.ser.close()
