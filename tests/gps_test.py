from sensors.gps import BitBangGPS

gps = BitBangGPS(gpio_pin=18)

try:
    print("[GPS Test] Waiting for fix...")
    lat, lon = gps.read(timeout=10)

    if lat is not None and lon is not None:
        print(f"[GPS Test] Latitude: {lat:.6f}, Longitude: {lon:.6f}")
    else:
        print("[GPS Test] No GPS fix within timeout")

finally:
    gps.close()
