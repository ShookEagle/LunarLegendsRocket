from utils.cross_platform_imports import RPi, pigpio, SMBus, Picamera2

# Example of using the imports
print("Libraries imported successfully!")

# Example test to ensure functionality:
try:
    GPIO = RPi.GPIO
    GPIO.setmode(GPIO.BCM)  # Example GPIO setup
    print("GPIO is available.")
except AttributeError:
    print("Running in mock mode: GPIO is mocked.")