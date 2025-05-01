import time
from sensors.bmp import Altimeter

alt = Altimeter()

print("[BMP Test] Starting... (Ctrl+C to stop)")
try:
    while True:
        altitude = alt.read_altitude()
        temperature = alt.read_bmp_temperature()
        pressure = alt.read_pressure()

        print(f"Pressure: {pressure:.2f} hPa | Temperature: {temperature:.2f} deg/C | Altitude: {altitude:.2f} m")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[BMP Test] Stopped.")
