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
    localizer.print_localized("startup")

    # Simulated initialization of modules
    localizer.print_localized("gps_init")

    # Mocked data
    latitude, longitude = 37.7749, -122.4194
    altitude = 123.45
    temperature = 25.0
    landing_message = f"I have landed my position is {latitude}, {longitude}"

    localizer.print_localized("gps_data", lat=latitude, lon=longitude)
    localizer.print_localized("altitude_data", altitude=altitude)
    localizer.print_localized("temperature_data", temperature=temperature)
    localizer.print_localized("sim_message_sent", message=landing_message)

    # Shutdown
    localizer.print_localized("shutdown")

if __name__ == "__main__":
    main()