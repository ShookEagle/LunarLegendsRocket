import time
import RPi.GPIO as GPIO

class Fuse:
    def __init__(self):
        self.GPIO_PIN = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PIN, GPIO.OUT)

    def trigger(self, duration=1):
        GPIO.output(self.GPIO_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.GPIO_PIN, GPIO.LOW)