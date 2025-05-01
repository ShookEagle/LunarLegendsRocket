import time
from sensors.bmp_trial import BMP

alt = BMP()

print("[BMP Test] Starting... (Ctrl+C to stop)")
try:
    while True:
        altitude = alt.read()

        print(f"Altitude: {altitude:.2f} m")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[BMP Test] Stopped.")
