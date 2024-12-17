# config/settings.py

import os

# General Settings
LANGUAGE = "en"  # Default language code (e.g., "en")

# Localization Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_PATH = os.path.join(BASE_DIR, "../locales/")  # Path to localization files

# Pin and Address Configuration (Example)
SIM800L_TX = 17
SIM800L_RX = 18
BMP388_ADDRESS = 0x77
MPU6050_ADDRESS = 0x68

# Camera Configuration
CAMERA_RESOLUTION = (1920, 1080)
CAMERA_FPS = 60