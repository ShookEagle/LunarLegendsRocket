import time
from sensors.bmp import Altimeter
from sensors.imu import IMU
from sensors.gps import GPS
from extras.fuse import Fuse
from data.logger import FlightLogger
from camera.dual_camera import PrebufferedRecorder
from communication.sim_module import SimModule

# === Config ===
LAUNCH_ACCEL_THRESHOLD = 6.0      # m/s²
LANDING_ACCEL_THRESHOLD = 2.0     # m/s² (low + stable)
LANDING_STABLE_SECONDS = 20.0     # time below threshold

print("[System] Booted — initializing sensors")
imu = IMU()
bmp = Altimeter()
gps = GPS()
fuse = Fuse()
sim = SimModule()
logger = FlightLogger(imu=imu, bmp=bmp)
camera = PrebufferedRecorder()
camera.start()


# === DATA ===
LAUNCH_ALTITUDE = bmp.read_altitude()
APOGEE_ALTITUDE = 0

# === Wait for launch ===
print("[System] Camera prebuffering... Waiting for launch")
sim.send_message("[System] Camera prebuffering... Waiting for launch")

while True:
    accel = imu.read_accel()
    vertical_accel = accel[1]
    net_vertical_accel = abs(vertical_accel - 9.8)

    if net_vertical_accel > LAUNCH_ACCEL_THRESHOLD:
        print(f"[Launch] Detected at {net_vertical_accel:.2f} m/s²")
        camera.trigger_save()
        camera.continue_recording()
        logger.start()
        break

    time.sleep(0.01)

# === Wait for Apogee ===
print("[System] In flight... Monitoring for apogee")

while True:
    if APOGEE_ALTITUDE < bmp.read_altitude():
        APOGEE_ALTITUDE = bmp.read_altitude()

    if APOGEE_ALTITUDE > bmp.read_altitude() + 50:
        fuse.trigger()
        break

    time.sleep(0.01)

# === Wait for Landing ===
stable_start = None

try:
    while True:
        accel = imu.read_accel()
        total_accel = (accel[0]**2 + accel[1]**2 + accel[2]**2)**0.5

        if (total_accel-9.8 < LANDING_ACCEL_THRESHOLD) and (bmp.read_altitude() < LAUNCH_ALTITUDE + 50):
            if stable_start is None:
                stable_start = time.time()
            elif time.time() - stable_start >= LANDING_STABLE_SECONDS:
                print("[Landing] Detected")
                break
        else:
            stable_start = None

        time.sleep(0.05)


# === Post-landing ===
    print("[System] Recording 20s post-landing...")
    sim.send_message(f"LANDED: I am at {gps.read()}")
    time.sleep(20)

finally:
    logger.stop()
    camera.close()
    print("[System] Shutdown complete.")