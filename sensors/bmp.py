import smbus2
import time
import struct


class Altimeter:
    def __init__(self, bus=1, address=0x77):
        self.bus = smbus2.SMBus(bus)
        self.address = address

        self._reset()
        time.sleep(0.01)

        self._read_calibration()
        self._configure_sensor()

        self.sea_level_pressure = self.read_pressure()

    def _reset(self):
        self._write_register(0x7E, 0xB6)  # Soft Reset
        time.sleep(0.01)

    def _configure_sensor(self):
        # oversampling settings: osr_p = 32x, osr_t = 2x, forced mode
        self._write_register(0x1B, 0x13)
        # output data rate (not important for forced)
        self._write_register(0x1C, 0x03)
        # iir filter settings (disabled)
        self._write_register(0x1D, 0x00)
        # enable pressure + temperature
        self._write_register(0x1F, 0x30)

    def _write_register(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def _read_block(self, reg, length):
        return self.bus.read_i2c_block_data(self.address, reg, length)

    def _read_register(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    def _read_calibration(self):
        calib = self._read_block(0x31, 21)
        coeffs = struct.unpack("<HHbhhbbHHbbhbb", bytes(calib))

        self.par_t1 = coeffs[0] / 2 ** 8
        self.par_t2 = coeffs[1] / 2 ** 30
        self.par_t3 = coeffs[2] / 2 ** 48

        self.par_p1 = (coeffs[3] - 2 ** 14) / 2 ** 20
        self.par_p2 = (coeffs[4] - 2 ** 14) / 2 ** 29
        self.par_p3 = coeffs[5] / 2 ** 32
        self.par_p4 = coeffs[6] / 2 ** 37
        self.par_p5 = coeffs[7] / 2 ** -3
        self.par_p6 = coeffs[8] / 2 ** 6
        self.par_p7 = coeffs[9] / 2 ** 8
        self.par_p8 = coeffs[10] / 2 ** 15
        self.par_p9 = coeffs[11] / 2 ** 48
        self.par_p10 = coeffs[12] / 2 ** 48
        self.par_p11 = coeffs[13] / 2 ** 65

    def _raw_read(self):
        # Start forced measurement
        self._write_register(0x1B, 0x13)

        # Wait until measurement ready
        while True:
            status = self._read_register(0x03)
            if (status & 0x60) == 0x60:
                break
            time.sleep(0.002)

        data = self._read_block(0x04, 6)

        raw_press = (data[2] << 16) | (data[1] << 8) | data[0]
        raw_temp = (data[5] << 16) | (data[4] << 8) | data[3]

        raw_press >>= 4
        raw_temp >>= 4

        return raw_press, raw_temp

    def _compensate_temp(self, adc_t):
        partial_data1 = adc_t - self.par_t1
        partial_data2 = partial_data1 * self.par_t2
        partial_data3 = partial_data1 * partial_data1
        partial_data4 = partial_data3 * self.par_t3
        t_lin = partial_data2 + partial_data4
        return t_lin

    def _compensate_pressure(self, adc_p, t_lin):
        partial_data1 = self.par_p6 * t_lin
        partial_data2 = self.par_p7 * t_lin * t_lin
        partial_data3 = self.par_p8 * t_lin * t_lin * t_lin
        partial_out1 = self.par_p5 + partial_data1 + partial_data2 + partial_data3

        partial_data4 = self.par_p2 * t_lin
        partial_data5 = self.par_p3 * t_lin * t_lin
        partial_data6 = self.par_p4 * t_lin * t_lin * t_lin
        partial_out2 = adc_p * (self.par_p1 + partial_data4 + partial_data5 + partial_data6)

        partial_data7 = adc_p * adc_p
        partial_data8 = self.par_p9 + self.par_p10 * t_lin
        partial_data9 = partial_data7 * partial_data8
        partial_data10 = partial_data7 * adc_p * self.par_p11

        pressure = partial_out1 + partial_out2 + partial_data9 + partial_data10
        return pressure

    def read_pressure(self):
        raw_press, raw_temp = self._raw_read()
        t_lin = self._compensate_temp(raw_temp)
        press = self._compensate_pressure(raw_press, t_lin)
        return press / 100.0  # Pa to hPa

    def read_temperature(self):
        _, raw_temp = self._raw_read()
        temp = self._compensate_temp(raw_temp)
        return temp

    def read_altitude(self):
        pressure = self.read_pressure()
        altitude = 44330.0 * (1.0 - (pressure / self.sea_level_pressure) ** 0.1903)
        return altitude