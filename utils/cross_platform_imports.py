import sys

if sys.platform != "linux":
    print("⚠️ Running in mock mode: Hardware-specific libraries are mocked.")
    import fake_rpi
    import fake_rpi.RPi as RPi  # Mock RPi.GPIO
    from unittest.mock import MagicMock

    # Mock Libraries that are Unavailable
    pigpio = MagicMock()
    SMBus = MagicMock()
    Picamera2 = MagicMock()

else:
    try:
        # raspberry pi OS libraries
        import RPi.GPIO as GPIO
        import pigpio
        from picamera2 import Picamera2
        from smbus import SMBus
    except ImportError as e:
        print("⚠️ Hardware libraries not found! Ensure this runs on Raspberry Pi OS.")
        raise e