# 🚀 **Rocket Telemetry and Video Recording System**

An advanced, modular rocket telemetry system designed for **data acquisition, real-time GPS tracking, altitude monitoring, and high-quality video recording**. Built with scalable hardware integration and robust software architecture, this system delivers **reliable, actionable data** for aerospace testing and analysis.

---

## 🌟 **Project Overview**

Our system leverages the **Raspberry Pi 4** as its central processing unit, integrating high-performance sensors and communication modules to create an **end-to-end telemetry solution**. This technology provides:

- **In-Flight Data Collection**: Altitude, motion sensing, and precise GPS tracking.  
- **Global Shutter Video Recording**: High-quality, distortion-free video capture.  
- **Post-Landing Communication**: Sends GPS coordinates via text message for location recovery.  

### **Why It Matters**  
Designed for **aerospace applications**, the system prioritizes modularity, accuracy, and scalability. Each component operates independently, ensuring seamless operation and maintainability for future enhancements.

---

## 🛠️ **Key Features**

- **Real-Time GPS Tracking**: Accurate location data powered by the NEO-M8J GPS module.  
- **Altitude and Environmental Monitoring**: High-precision altitude and temperature readings using the Adafruit BMP388 sensor.  
- **Motion Sensing**: Accelerometer and gyroscope integration with the MPU6050 module.  
- **Distortion-Free Video**: IMX296 Global Shutter Camera for 1080p, 60fps recording.  
- **Post-Landing Location Recovery**: GPS coordinates transmitted via the SIM800L GSM module.  
- **Secure Power Management**: A key-operated switch ensures controlled system startup.  
- **Modular Codebase**: Designed with scalability in mind, each component is independently managed.  

---

## 🔩 **System Components**

| **Component**                 | **Purpose**                          |
|-------------------------------|--------------------------------------|
| **Raspberry Pi 4 (8GB)**      | Central processing and coordination  |
| **IMX296 Global Shutter Camera** | High-quality video recording       |
| **Pololu U3V50F5**            | Power stabilization (5V conversion)  |
| **Adafruit BMP388**           | Altitude and temperature monitoring  |
| **SIM800L**                   | GSM-based communication module       |
| **NEO-M8J GPS Module**        | Real-time location tracking          |
| **MPU6050**                   | Accelerometer and gyroscope data     |
| **Adafruit Perma-Proto HAT**  | GPIO pin expansion for connections   |
| **Key-Operated Switch**       | Secure system startup control        |

---

## 🎥 **Video Recording Excellence**  

The **IMX296 Global Shutter Camera** provides:  
- **Resolution**: 1080p (1.58 MP, color sensor)  
- **Frame Rate**: 60 fps for smooth motion capture  
- **Wide Field of View**: Customizable lenses achieve a **100° viewing angle**  

This ensures high-quality, distortion-free recordings—critical for analyzing high-speed flight events.

---

## 🖥️ **System Workflow**

1. **Startup**: Controlled startup via a secure key-operated switch.  
2. **Launch Detection**: Sensors initialize and monitor environmental data.  
3. **In-Flight**:  
   - Collects and records altitude, motion, and GPS data.  
   - Simultaneously records high-speed, high-resolution video.  
4. **Post-Landing**:  
   - Sends precise landing GPS coordinates via a text message.  
   - Logs all telemetry data for post-analysis.

---

## 📊 **Scalable Design**  

Our modular architecture ensures easy integration of additional sensors, communication systems, or custom features. The system can be adapted for:

- Aerospace prototyping  
- Educational rocket launches  
- Environmental data collection  
- Real-time video telemetry systems  

Each hardware module has an independent codebase, allowing for rapid scaling and future enhancements.

---

## 💡 **Technologies Leveraged**

- **Python**: Fast, reliable system control and hardware communication.  
- **Pigpio**: GPIO and UART management for sensor integration.  
- **NMEA Parsing**: Efficient processing of GPS data.  
- **Adafruit CircuitPython Libraries**: Simplifies sensor communication.  

---

## 📧 **Contact Information**

For more information or partnership opportunities:

- **Name**: Reece DeAlmeida  
- **Email**: [reece.dealmeida@yahoo.com](mailto:reece.dealmeida@yahoo.com)  

