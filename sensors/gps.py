import serial
import time
import re

class GPS:
    def __init__(self, port="/dev/ttyAMA3", baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)  # Allow time for the GPS module to initialize

    def read_line(self):
        """Read a line from the GPS module."""
        try:
            line = self.ser.readline()
            return line.decode('ascii', errors='ignore').strip()
        except Exception as e:
            print(f"Error reading line: {e}")
            return None

    def parse_GPGGA(self, sentence):
        """
        Parse GPGGA sentence to extract time, latitude, longitude, fix status, and number of satellites.
        """
        if not sentence.startswith('$GPGGA'):
            return None

        parts = sentence.split(',')
        if len(parts) < 15:
            return None

        try:
            time_utc = parts[1]
            lat = self._convert_to_decimal(parts[2], parts[3])
            lon = self._convert_to_decimal(parts[4], parts[5])
            fix_quality = int(parts[6])
            num_satellites = int(parts[7])

            return {
                'time_utc': time_utc,
                'latitude': lat,
                'longitude': lon,
                'fix_quality': fix_quality,
                'num_satellites': num_satellites
            }
        except (ValueError, IndexError) as e:
            print(f"Error parsing GPGGA: {e}")
            return None

    def _convert_to_decimal(self, raw_value, direction):
        """
        Convert raw NMEA coordinate to decimal degrees.
        """
        if not raw_value or not direction:
            return None

        try:
            degrees = int(raw_value[:2])
            minutes = float(raw_value[2:])
            decimal = degrees + (minutes / 60)
            if direction in ['S', 'W']:
                decimal *= -1
            return decimal
        except ValueError as e:
            print(f"Error converting to decimal: {e}")
            return None

    def close(self):
        """Close the serial connection."""
        self.ser.close()
