import pigpio
import pynmea2
import time

class BitBangGPS:
    def __init__(self, gpio_pin: int, baudrate: int = 9600):
        self.gpio_pin = gpio_pin
        self.baudrate = baudrate
        self.pi = pigpio.pi()

        if not self.pi.connected:
            raise RuntimeError("Failed to connect to pigpio daemon")

        self.pi.bb_serial_read_open(self.gpio_pin, self.baudrate)
        print(f"[GPS] Listening on GPIO {self.gpio_pin} at {self.baudrate} baud")

    def read(self, timeout=5):
        """
        Read and parse NMEA sentence to get latitude and longitude.
        Returns (latitude, longitude) or (None, None) if unavailable.
        """
        start_time = time.time()
        buffer = b""

        while time.time() - start_time < timeout:
            count, data = self.pi.bb_serial_read(self.gpio_pin)
            if count > 0:
                buffer += data
                lines = buffer.split(b'\n')
                buffer = lines[-1]  # Save incomplete line

                for line in lines[:-1]:
                    try:
                        sentence = line.decode('ascii', errors='ignore').strip()
                        if sentence.startswith('$GPRMC') or sentence.startswith('$GPGGA'):
                            msg = pynmea2.parse(sentence)
                            lat = getattr(msg, 'latitude', None)
                            lon = getattr(msg, 'longitude', None)
                            if lat and lon:
                                return lat, lon
                    except (UnicodeDecodeError, pynmea2.ParseError):
                        continue
            time.sleep(0.05)

        return None, None

    def close(self):
        self.pi.bb_serial_read_close(self.gpio_pin)
        self.pi.stop()
        print("[GPS] Closed connection")
