import serial
import time

class SIM800L:
    def __init__(self, port="/dev/serial0", baudrate=9600):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(1)
        self.init_module()

    def send_at(self, command, delay=1):
        self.ser.write((command + "\r\n").encode())
        time.sleep(delay)
        return self.ser.read_all().decode()

    def init_module(self):
        self.send_at("AT")            # Basic check
        self.send_at("AT+CMGF=1")     # Set SMS text mode
        self.send_at("AT+CSCS=\"GSM\"")  # Set char set

    def send_sms(self, phone_number, message):
        self.send_at(f'AT+CMGS="{phone_number}"')
        time.sleep(1)
        self.ser.write((message + "\x1A").encode())  # \x1A is CTRL+Z (end of message)
        time.sleep(5)  # Allow time to send
