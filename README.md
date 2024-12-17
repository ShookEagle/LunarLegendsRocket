# 🚀 **Raspberry Pi Modular Rocket System**

An innovative and modular rocket telemetry system designed for **data collection, GPS tracking, altitude monitoring, and video recording** using the **Raspberry Pi 4** and a suite of sensors. Built with a focus on modularity, clean code structure, and hardware integration.

---

## 🌟 **Project Overview**

This project demonstrates my ability to design and implement a **real-time hardware integration system** for rockets using a Raspberry Pi. The system handles **GPS tracking**, **altitude measurement**, **video recording** with a global shutter camera, and **communication** through a SIM module.

It is **fully modular**, meaning each hardware component operates independently within its own module. The code is clean, well-organized, and easily scalable.

---

## 🛠️ **Key Features**

- **GPS Tracking**: Real-time location acquisition via NEO-M8J GPS module.
- **Altitude Measurement**: High-precision altitude data using the Adafruit BMP388 sensor.
- **Motion Sensing**: Gyroscope and accelerometer integration with the MPU6050.
- **Video Recording**: High-quality video capture with the IMX296 color global shutter camera.
- **SIM Communication**: Sends location coordinates post-landing via text message.
- **Secure Startup**: Power system managed with a **key-operated switch**.
- **Modular Codebase**: Each component has its own file, keeping the system scalable and maintainable.

---

## 🔩 **Hardware Components**

| Component                     | Function                         |
|-------------------------------|----------------------------------|
| **Raspberry Pi 4 (8GB)**      | System processing and control    |
| **IMX296 Color Global Shutter** | High-quality video recording    |
| **Pololu U3V50F5**            | Stable 5V power conversion       |
| **Adafruit BMP388**           | Altitude data (altimeter)        |
| **SIM800L**                   | SIM-based text communication     |
| **NEO-M8J-0 GPS**             | Real-time location tracking      |
| **MPU6050**                   | Motion data: gyro + accelerometer|
| **Adafruit Perma-Proto HAT**  | GPIO pin expansion and connections|
| **Key Switch**                | Secure system startup            |

---

## 🧩 **Modular Code Design**

This project is built with modularity in mind. Each hardware component is implemented in its own file, making the system clean, scalable, and easy to debug.

```plaintext
project/
│
├── main.py                 # Main controller (orchestrates all modules)
│
├── components/             # Modular components
│   ├── gps.py              # Handles GPS data
│   ├── bmp388.py           # Altitude and temperature readings
│   ├── mpu6050.py          # Gyroscope/accelerometer readings
│   ├── sim800l.py          # SIM module messaging
│   ├── camera.py           # Video recording control
│   └── power.py            # Power management logic
│
├── utils/                  # Utility scripts
│   ├── localizer.py        # Centralized messaging system
│   └── logger.py           # Logging setup for debugging
│
├── config/                 # Configuration settings
│   └── settings.py         # Pin numbers, addresses, etc.
│
└── README.md               # Project documentation
```
Each module focuses on one task:
- **gps.py:** Fetches and parses GPS coordinates.
- **bmp388.py:** Reads altitude and temperature from BMP388.
- **camera.py:** Controls the IMX296 global shutter camera.
- **sim800l.py:** Manages SIM-based communication (e.g., sending GPS data after landing).
- **power.py:** Manages power handling logic.

## 🎥 **Highlight: Camera Module**
The IMX296 Global Shutter Camera enables high-quality video recording with:
- **Resolution:** 1.58 MP (color sensor)
- **Frame Rate:** 60 fps
- **Wide-Angle Lens:** Captures a 100° field of view.

This ensures distortion-free, high-speed video suitable for rocket launches.

## 🖥️ **System Workflow**
1. **Startup:** System powers up when the key switch is turned on.
2. **Waiting for Launch:** The system initializes and monitors telemetry.
3. **In Flight:** Collects real-time data (altitude, motion, location) and records video.
4. **Post-Landing:**
   - Sends GPS coordinates via the SIM800L module using text messages.
   - Logs data for analysis.

## 💡 **Technologies Used**
- **Python:** Programming language for system control.
- **Pigpio:** For managing GPIO pins and software UART.
- **Adafruit Libraries:** For sensor communication and data handling.
- **NMEA Parsing:** GPS data parsing using pynmea2.

## 🚀 **Skills Demonstrated**
- **Hardware Integration:** Connecting and configuring multiple sensors and modules.
- **Modular Code Design:** Clean, scalable, and maintainable Python codebase.
- **GPIO Control:** Effective use of Raspberry Pi GPIO pins for hardware communication.
- **Power Management:** Implementing a secure startup system with a key switch.
- **Data Handling:** Real-time sensor data acquisition, video recording, and post-processing.

## 🏆 **Why This Project Stands Out**
This project showcases my ability to:
- Combine software and hardware integration to solve a real-world problem.
- Develop modular, maintainable, and clean code.
- Integrate advanced hardware like the IMX296 global shutter camera.
- Implement secure power management and communication systems.

## 📧 **Contact**
- **Name:** Reece DeAlmeida
- **Email:** reece.dealmeida@yahoo.com