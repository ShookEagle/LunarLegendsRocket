from utils.cross_platform_imports import RPi, pigpio, SMBus, Picamera2
from utils.localizer import Localizer
from config.settings import LANGUAGE

# Example of using the imports
print("Libraries imported successfully!")

# Example test to ensure functionality:
try:
    GPIO = RPi.GPIO
    GPIO.setmode(GPIO.BCM)  # Example GPIO setup
    print("GPIO is available.")
except AttributeError:
    print("Running in mock mode: GPIO is mocked.")


def main():
    # Initialize the localizer
    localizer = Localizer(language=LANGUAGE)

    # Print startup message
    print(localizer.get_message("startup"))

    # Simulated initialization of modules
    print(localizer.get_message("gps_init"))

    # Mocked data
    latitude, longitude = 37.7749, -122.4194
    altitude = 123.45
    temperature = 25.0
    landing_message = f"I have landed my position is {latitude}, {longitude}"

    print(localizer.get_message("gps_data", lat=latitude, lon=longitude))
    print(localizer.get_message("altitude_data", altitude=altitude))
    print(localizer.get_message("temperature_data", temperature=temperature))
    print(localizer.get_message("sim_message_sent", message=landing_message))

    # Shutdown
    print(localizer.get_message("shutdown"))

if __name__ == "__main__":
    main()