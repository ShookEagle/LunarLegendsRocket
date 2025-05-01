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
        print(f"[GPS] BitBang serial opened on GPIO {self.gpio_pin}")

    def read(self, timeout=5):
        start_time = time.time()
        buffer = b""

        while time.time() - start_time < timeout:
            (count, data) = self.pi.bb_serial_read(self.gpio_pin)

            if count > 0:
                buffer += data
                lines = buffer.split(b'\n')
                buffer = lines[-1]  # incomplete last line

                for line in lines[:-1]:
                    try:
                        sentence = line.decode('ascii', errors='ignore').strip()

                        if sentence.startswith('$GPGGA') or sentence.startswith('$GPRMC'):
                            msg = pynmea2.parse(sentence)

                            if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                                lat = msg.latitude
                                lon = msg.longitude
                                if lat != 0.0 and lon != 0.0:
                                    return lat, lon
                    except pynmea2.ParseError:
                        continue

            time.sleep(0.1)

        return None, None

    def close(self):
        self.pi.bb_serial_read_close(self.gpio_pin)
        self.pi.stop()
        print("[GPS] BitBang serial closed")
