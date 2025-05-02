import serial
import time

ser = serial.Serial("/dev/ttyAMA1", 9600, timeout=1)

print("Starting GPS read loop...\n")

try:
    while True:
        line = ser.readline()
        if line:
            print(">>", line.decode(errors="ignore").strip())
        else:
            print("...waiting...")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    ser.close()
