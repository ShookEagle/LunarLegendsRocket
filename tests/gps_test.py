if __name__ == "__main__":
    gps = GPS()
    try:
        latitude, longitude = gps.read()
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    except KeyboardInterrupt:
        print("GPS reading stopped by user.")
    finally:
        gps.close()
