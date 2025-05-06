import serial
import time

# Configure the serial connection
ser = serial.Serial(
    port='/dev/ttyAMA3',      # Replace with your serial port
    baudrate=9600,
    timeout=1                 # Timeout in seconds
)

# Continuous read loop
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            print(line)
        time.sleep(0.1)  # Small delay to prevent high CPU usage
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()