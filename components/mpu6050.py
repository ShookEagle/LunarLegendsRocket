import smbus

class MPU6050:
    def __init__(self, bus=1, address=0x68):
        self.bus = smbus.SMBus(bus)
        self.address = address
        self._initialize_sensor()

    def _initialize_sensor(self):
        # Write to power management register to wake up the MPU6050
        self.bus.write_byte_data(self.address, 0x6B, 0)
        # Set accelerometer configuration (±2g)
        self.bus.write_byte_data(self.address, 0x1C, 0)
        # Set gyroscope configuration (±250°/s)
        self.bus.write_byte_data(self.address, 0x1B, 0)

    def _read_raw_data(self, register):
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)
        value = (high << 8) | low
        if value > 32768:
            value -= 65536
        return value

    def get_acceleration(self):
        ax = self._read_raw_data(0x3B) / 16384.0
        ay = self._read_raw_data(0x3D) / 16384.0
        az = self._read_raw_data(0x3F) / 16384.0
        return {'x': ax, 'y': ay, 'z': az}

    def get_gyroscope(self):
        gx = self._read_raw_data(0x43) / 131.0
        gy = self._read_raw_data(0x45) / 131.0
        gz = self._read_raw_data(0x47) / 131.0
        return {'x': gx, 'y': gy, 'z': gz}
