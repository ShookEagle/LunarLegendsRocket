import serial
import pynmea2

# Configure the serial port to which the GPS module is connected
serial_port = '/dev/serial0'  # Update this if your GPS module is connected to a different port
baud_rate = 9600  # Ensure this matches your GPS module's baud rate

def read_gps_data():
    # Open the serial port
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        while True:
            try:
                # Read a line of data from the GPS
                line = ser.readline().decode('ascii', errors='replace').strip()
                # Check if the line is a GGA sentence
                if line.startswith('$GPGGA'):
                    msg = pynmea2.parse(line)
                    latitude = msg.latitude
                    longitude = msg.longitude
                    altitude = msg.altitude
                    num_sats = msg.num_sats
                    print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude} meters, Satellites: {num_sats}")
            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")
            except serial.SerialException as e:
                print(f"Serial error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == '__main__':
    read_gps_data()
