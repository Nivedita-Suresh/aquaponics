# **1. Water Level Monitoring & Pump Control Module**

**Author:** Nivedita Suresh 

## Overview
This module is a component of the aquaponics system and is responsible for automatically monitoring and maintaining the water level. Proper water level control is essential to ensure the health of both plants and fish while preventing overflow or water shortages.

## Working Principle
The system continuously monitors the water level using a **potentiometer**, which is used to simulate a real water level sensor. The potentiometer is connected to the ADC pin of the Raspberry Pi Pico, allowing analog values to be read and converted into a percentage-based water level (0–100%).An **LED** is used to simulate the pump operation instead of an actual relay and pump for safe testing and demonstration purposes.

## Control Logic
Based on the measured water level, the pump operation is controlled automatically:
- When the water level falls below **30%**, the pump is turned **ON**
- When the water level rises above **70%**, the pump is turned **OFF**
- For water levels between **30% and 70%**, the pump remains in a **HOLD** state


## Simulation and Output
The system provides real-time feedback by printing the current water level and pump status to the console. Adjusting the potentiometer simulates changes in water level, allowing easy observation of pump behavior during testing.

## circuit design
<img width="735" height="494" alt="image" src="https://github.com/user-attachments/assets/ca35723a-9b5a-44d8-8b83-530722cea55d" />










# **2. Water pH Monitoring Module** 

**Author:** Navya VK

## Overview

This module is a part of the aquaponics system and is responsible for monitoring the water pH level to ensure a healthy environment for fish and plants. Maintaining an appropriate pH range is crucial for fish survival and efficient nutrient absorption by plants. This module demonstrates pH monitoring using a simulated setup suitable for testing and academic implementation.

## Working Principle

The system continuously monitors the pH level using a potentiometer, which is used to simulate the behavior of a real pH sensor. The **potentiometer** is connected to the ADC pin of the Raspberry Pi Pico, allowing analog voltage values to be read and converted into corresponding pH values on a scale of 0 to 14.
An **LED** is used as a visual alert indicator to represent abnormal pH conditions instead of using an actual alarm system, making the setup safe and simple for simulation purposes.

## Control Logic

Based on the calculated pH value, the system classifies the water condition as follows:

- When the pH value lies between **6.5** and **8.5**, the pH level is considered **NORMAL**

- When the pH value falls below **6.5**, the water is ACIDIC, and the **LED alert is activated**

- When the pH value rises above **8.5**, the water is ALKALINE, and the **LED alert is activated**

- The **LED** blinks to indicate abnormal pH conditions and remains **OFF** when the pH level is within the safe range.

## Simulation and Output

The system provides real-time feedback by displaying the current pH value and its corresponding status (Normal, Acidic, or Alkaline) on the serial console. Adjusting the potentiometer simulates changes in water pH, enabling easy observation of system response and alert indication during testing and demonstration.

## Circuit Design
<img width="735" height="494" alt="pH pinout diagram" src="https://github.com/user-attachments/assets/14385feb-b558-4073-bbef-767395da7609" />




# **3. Water Temperature Monitoring & Alert Module**

**Author:** Nikhil H  

---

### Overview  
The Water Temperature Monitoring & Alert Module is a critical part of the aquaponics automation system. It continuously measures the water temperature in real time to ensure a healthy environment for both fish and plants. Maintaining an optimal temperature range is essential for fish metabolism and efficient nutrient absorption in plants.  

The module also includes an automated alert mechanism that warns the user whenever the temperature exceeds safe limits.

---

### Working Principle  
This system uses the **DS18B20 digital temperature sensor** interfaced with the **Raspberry Pi Pico**. Unlike analog temperature sensors, the DS18B20 operates using the **1-Wire communication protocol**, enabling accurate digital temperature readings with minimal wiring.

- **Data Acquisition:**  
  The Pico reads temperature values from the DS18B20 through a single data pin (**GP22**). A **4.7 kΩ pull-up resistor** is used to maintain signal stability and ensure reliable communication.

- **Visual Alert Mechanism:**  
  An LED is included in the circuit as a **Critical Temperature Indicator**, simulating an automated cooling trigger or manual alarm system.

---

### Control Logic  
The firmware continuously polls the sensor and compares the temperature against a defined threshold:

- **Normal State:**  
  If the temperature remains **between 30°C and 25°C**, the system stays in monitoring mode and the Alert LED remains **OFF**.

- **Alert State:**  
  If the temperature reaches either **above 30°C** or **below 25°C** , the system activates a high-priority warning. The LED turns **ON**, and a warning message is printed to the serial console.

- **Error Handling:**  
  The code verifies whether the sensor is properly connected. If no ROM address is detected, the system reports a **"Device Disconnected"** error.

---

### Simulation and Output  
The module is simulated using **Wokwi** with **MicroPython**. Within the simulation:

- The user can manually adjust the DS18B20 temperature value by clicking and sliding the sensor control.
- The Serial Console displays continuous real-time temperature readings in **degrees Celsius (°C)**.
- The LED provides immediate visual feedback when the temperature exceeds the critical threshold.

---

### Circuit Design  
<img width="735" height="494" alt="Screenshot 2026-02-07 164303" src="https://github.com/user-attachments/assets/c642e0e2-8c6f-438f-86a3-2d345c7f8cc8" />

# **4. Pump Logic**

**Author:** Nivedita Suresh

### Overview
This aquaponics system uses a **single submersible water pump** to circulate water between the fish tank and the grow beds. The pump is placed inside the fish tank and is responsible for lifting nutrient-rich water to the grow beds, while the return flow to the tank occurs naturally through **gravity-based drainage**. This simple and efficient circulation mechanism ensures continuous nutrient delivery to plants and maintains a healthy aquatic environment for the fish.

### Pump Operation
For the current small-scale setup (one fish tank with one or two grow beds and a minimal fish load), the pump operates in a **continuous ON mode**. Continuous circulation provides:
- Stable water levels in the fish tank
- Consistent nutrient supply to plant roots
- Improved oxygenation of water
- Reduced stress on fish due to sudden flow changes

An optional enhancement to this approach is a **timed flood-and-drain cycle**, where the pump operates for a fixed duration (e.g., ON for a few minutes and OFF for a few minutes). This mode can improve root aeration and reduce power consumption, but it is not strictly required for the current system scale.

### Use of a Single Pump
Only **one pump** is used in the system due to the following reasons:
- Gravity efficiently returns water from the grow beds back to the fish tank
- Additional pumps for drainage are unnecessary and increase system complexity
- A single pump is sufficient to handle the low flow-rate requirements of a small aquaponics setup
- Fewer components reduce power consumption, cost, and maintenance effort

This design choice improves overall system reliability while keeping the architecture simple and easy to manage.

### Complexity Avoidance and Design Justification
Advanced aquaponics systems often use multiple pumps, solenoid valves, and closed-loop control based on real-time sensor feedback. However, such complexity was intentionally avoided in this project because:
- The system operates at a very small scale
- The risk of overflow or dry-run conditions is minimal
- Over-automation increases failure points and debugging difficulty
- Simplicity enhances long-term stability and ease of use


### Summary
The pump logic prioritizes **simplicity, reliability, and energy efficiency**. By using a single continuously operating pump and gravity-assisted drainage, the system achieves effective water circulation without unnecessary complexity. Sensor data is leveraged for monitoring and alerts rather than direct actuation, making the design well-suited for small-scale aquaponics applications and future scalability.

# **5. Integrated Water Monitoring Module**

The individual modules for water temperature, pH level, and water level monitoring were successfully integrated into a single program running on the Raspberry Pi. This integration allows all sensor data to be collected and processed together, ensuring synchronized readings and simpler system management.

The combined module displays water temperature, pH value, water level condition, and overall system status through a serial/terminal output. This confirms correct sensor operation and system stability after integration.

As a next stage, the integrated sensor data will be sent to a mobile application for real-time remote monitoring. This will enable users to track water temperature, pH level, and water level directly from their phones, forming the basis for future IoT-based control and alert features.

<img width="754" height="547" alt="image" src="https://github.com/user-attachments/assets/44a43a8c-f42c-4cd1-b724-08713bcc29f7" />


 # **6. Basic Logic of Automatic Fish Feeding System**

 **Author:** Nezrin Shareef

 Objective

To **automatically feed fish at fixed time intervals** in an aquaponic system without human intervention, ensuring uniform feeding and reduced feed wastage.

 ## Components Involved

* Microcontroller (Arduino / ESP32)
* Servo motor (for feed dispensing)
* Real Time Clock (RTC) module **OR** internal timer
* Power supply

---

## Working Logic 

### Step 1: System Initialization

* Initialize microcontroller
* Set feeding times (e.g., morning and evening)
* Set servo motor initial position (closed state)

---

### Step 2: Time Monitoring

* Continuously monitor current time using:

  * RTC module **or**
  * Internal delay/timer function

---

### Step 3: Feeding Condition Check

* Compare current time with predefined feeding time

```
IF (current time == feeding time)
    Activate feeder
ELSE
    Keep feeder OFF
```

---

### Step 4: Feed Dispensing

* Rotate servo motor by a fixed angle
* Feed is released into fish tank
* Maintain rotation for a fixed duration (e.g., 2–3 seconds)

---

### Step 5: Reset Feeder

* Rotate servo back to original position
* Stop feeding action

---

### Step 6: Repeat Cycle

* System waits for next feeding time
* Process repeats automatically

---

## Logic in Simple Pseudocode

```
Start
Initialize servo motor
Set feeding times

Loop:
   Read current time
   If time matches feeding time:
       Rotate servo to open feeder
       Delay for feed release
       Rotate servo back to close feeder
   End if
End loop

 
## Optional Safety Logic 


If (water level is LOW)
   Skip feeding
If (temperature is HIGH)
   Reduce feeding duration

## Key Advantages

* Timely and uniform feeding
* Reduced manual effort
* Prevents overfeeding
* Improves fish health
```

# 7. Smart Aquaponics Dashboard – Initial Version

**Author: **Nivedita Suresh, Nikhil H

---

## Overview

This module represents the initial graphical user interface (GUI) prototype of the Smart Aquaponics System. The dashboard provides a centralized platform to visualize key environmental parameters and monitor overall system health.

Developed using Flutter, this interface establishes the structural and visual foundation for real-time aquaponics monitoring. The primary objective of this version is to implement a clean, responsive, and modern dashboard layout capable of displaying sensor data and reflecting system status dynamically.

---

## Working Principle

The dashboard displays three primary environmental parameters:

- Water Level (%)
- pH Level
- Temperature (°C)

In this initial implementation, these values are simulated within the application to demonstrate interface behavior and control logic. The architecture is designed to allow seamless integration with real-time sensor data in later stages.

The system also includes a visual pump status indicator represented by a toggle-style switch on the interface.

---

## Control Logic (Prototype Version)

In the current simulation logic:

- When the water level falls below 65%, the pump status changes to ON.
- When the water level rises above the defined threshold, the pump state updates accordingly within the UI.

This logic is implemented purely for simulation and demonstration of dynamic UI behavior.

---

## Final Product Logic (Planned Implementation)

In the final hardware-integrated system:

- The pump will remain continuously ON.
- No ON/OFF switching based on water level will be implemented.

The pump will operate continuously to:

- Ensure constant water circulation
- Maintain adequate aeration for fish
- Support stable nutrient distribution for plants
- Prevent stagnation within the aquaponics system

Water level monitoring will continue to be used for alerting and diagnostics rather than direct pump control.

---

## Simulation and Output

This prototype provides real-time visual feedback within the dashboard interface:

- Water level displayed as a percentage
- pH level shown with qualitative status (e.g., Optimal)
- Temperature displayed in Celsius
- Pump status visually represented via a toggle indicator
- System connectivity status displayed as "Connected"

Adjusting simulated values within the application demonstrates dynamic UI updates and state management behavior.

This simulation stage ensures that user interface logic and presentation are validated prior to full hardware integration.

---

## Version Control

The project is maintained using Git-based version control to ensure:

- Structured development workflow
- Change tracking and revision history
- Collaborative feature development
- Code stability and maintainability

The repository will continue evolving toward a fully integrated, production-ready Smart Aquaponics Monitoring Dashboard.

# 8.Smart Aquaponics Dashboard (Flutter Simulation)                
**Author:** Nivedita Suresh
## Project Overview

The **Smart Aquaponics Dashboard** is a Flutter-based mobile application designed to simulate and monitor key parameters of an aquaponics system. It provides real-time sensor simulation, pump control, alert and log tracking, and data visualization.

This version is fully simulated and serves as a foundation for future IoT integration.

---

## Features Implemented

### Sensor Simulation
- **Water Level:** Simulated between 45%–60%; generates a red alert if below 65%.
- **pH Level:** Simulated between 6.5–7.5; status categories: Optimal, Balanced, Out of Range.
- **Temperature:** Simulated for Kerala climate conditions (26°C–34°C); status categories: Optimal, Warning, Critical.

### Pump Control
- Pump is ON by default.
- Manual toggle available to simulate control.
- Clicking generates log entries.

### Alerts and Logs
- Logs generated for water level, pH, temperature, and pump state changes.
- Displays timestamp, status message, color, and icon.
- Maximum 20 recent logs shown.

### Sensor Graph
- Line chart shows:
  - Water Level (green)
  - pH Level (blue)
- Rolling window of last 24 readings.
- Curved line visualization for clarity.

### Automatic Data Refresh
- Sensor simulation updates every 3 seconds using `Timer.periodic`.

---

## Architecture

- **Models:** `LogEntry` for alert storage.
- **Controller:** Simulates sensors, manages alerts, and updates graph data.
- **UI Layer:** Stateful dashboard with cards for stats, logs, and graphs.

---
## Screenshots
<img width="1578" height="737" alt="Screenshot 2026-02-25 101906" src="https://github.com/user-attachments/assets/23965327-16aa-491b-9097-6c781a6d846c" />
<img width="1583" height="331" alt="Screenshot 2026-02-25 101929" src="https://github.com/user-attachments/assets/4babf3f7-dc7d-4a72-ba18-dcfa0d888eb5" />
<img width="1920" height="1080" alt="Screenshot 2026-02-25 105548" src="https://github.com/user-attachments/assets/d8f55e5f-d752-4090-8b1e-89096e22d371" />

---
## link for the app 
https://github.com/Nivedita-Suresh/aquaponics_app.gitrepo

---
## Dependencies

---
```yaml
dependencies:
  flutter:
    sdk: flutter
  fl_chart: ^0.60.0
  intl: ^0.18.0
```

# 9.Pico + ESP8266 LED Control using Flutter

**Author:** Nivedita Suresh, Nikhil H  
**Repository Name:** https://github.com/Nivedita-Suresh/pico-esp8266-led-control/tree/main

---

## Overview

This project demonstrates controlling an LED connected to a **Raspberry Pi Pico** using an **ESP8266 WiFi module** in Access Point mode.  

A **Flutter Windows desktop application** sends HTTP requests to the ESP8266, which forwards them to the Pico via UART. The Pico processes the requests and controls the LED accordingly.  

This creates a simple **IoT communication pipeline** over a local WiFi network without requiring internet access.

---

## System Architecture

Flutter App (HTTP Client)  
↓  
ESP8266 (WiFi AP + Web Server)  
↓  
Raspberry Pi Pico (MicroPython Controller)  
↓  
LED  

---

## Network Configuration

- **SSID:** Pico_LED  
- **Password:** 12345678  
- **IP Address:** 192.168.4.1  
- **Port:** 80  

> The computer must connect to the `Pico_LED` network before running the Flutter app.

---

## Working Principle

1. The Flutter app shows a toggle switch for LED control.  
2. Toggling sends `/on` or `/off` HTTP requests.  
3. The ESP8266 receives the request and forwards it to the Pico via UART.  
4. The Pico controls the LED and sends a response back.  
5. The Flutter app updates the LED state and connection indicator.

---

## Circuit Diagram

<img width="1589" height="1080" alt="image" src="https://github.com/user-attachments/assets/b183c33a-6501-4161-8177-fdb64a61166e" />

---

## References

1. https://microcontrollerslab.com/esp8266-wifi-module-raspberry-pi-pico-web-server/
2. D. R. Loker, "Raspberry Pi Pico as an IoT Device," in Proceedings of the 2023 ASEE Annual Conference & Exposition, Baltimore, MD, USA, Jun. 2023. [Online]. Available: https://peer.asee.org/raspberry-pi-pico-as-an-iot-device
3. P. D. P. Adi, A. Kristiyanto, A. Sopandi, I. Nirmala, M. Tahir, and E. Y. Wijaya, "Performance Evaluation of Raspberry Pi Pico for Internet of Things and Its Analysis," in Proceedings of the 2024 4th International Conference on ..., IEEE, 2024. [Online]. Available: https://ieeexplore.ieee.org/


---

## Conclusion

This project demonstrates a complete IoT setup with:

- Real-time LED control via WiFi  
- UART communication between ESP8266 and Raspberry Pi Pico  
- Simple HTTP-based client-server architecture  
- Integration of embedded systems with a Flutter desktop application  

It serves as a foundation for expanding into larger IoT systems and modular microcontroller projects.



# 10.Pico + ESP8266 Smart Aquaponics Monitoring Dashboard

**Author:** Nivedita Suresh  
**Repository Name:** https://github.com/Nivedita-Suresh/aquaponics_app.git

---

## Overview

This project demonstrates a **Smart Aquaponics Monitoring System** using a **Raspberry Pi Pico**, **ESP8266 WiFi module**, and a **Flutter desktop dashboard**.

The Raspberry Pi Pico collects sensor data from:

- **HC-SR04 Ultrasonic Sensor** for water level measurement
- **DS18B20 Temperature Sensor** for water temperature monitoring

The Pico communicates with an **ESP8266 module via UART**, which hosts a **WiFi Access Point and HTTP server**.  

A **Flutter dashboard application** connects to this local network and periodically retrieves sensor data through HTTP requests, displaying real-time values and graphical history charts.

This setup enables **real-time monitoring of aquaponics parameters without requiring internet access**, making it suitable for embedded IoT environments.

---

## System Architecture

Flutter Desktop Dashboard (HTTP Client)  
↓  
ESP8266 (WiFi Access Point + HTTP Server)  
↓  
Raspberry Pi Pico (MicroPython Controller)  
↓  
Sensors (HC-SR04, DS18B20)

---

## Hardware Components

- Raspberry Pi Pico
- ESP8266 WiFi Module (ESP-01 / ESP8266)
- HC-SR04 Ultrasonic Distance Sensor
- DS18B20 Waterproof Temperature Sensor
- Breadboard & Jumper Wires

---

## Software Components

### Embedded System

- **MicroPython** running on Raspberry Pi Pico
- UART communication between Pico and ESP8266
- ESP8266 controlled using **AT Commands**

### Desktop Application

- **Flutter**
- **HTTP package** for REST requests
- **FL Chart package** for real-time graphs
- **thonny**
---

## Network Configuration

- **SSID:** Pico_Sensors  
- **Password:** 12345678  
- **IP Address:** 192.168.4.1  
- **Port:** 80  

> The computer must connect to the `Pico_Sensors` WiFi network before running the Flutter dashboard.

---

## Working Principle

1. The **ESP8266 starts in Access Point mode** and hosts an HTTP server.
2. The **Raspberry Pi Pico communicates with the ESP8266 using UART**.
3. When the Flutter app sends an HTTP request: http://192.168.4.1
4. The ESP8266 forwards the request to the Pico.
5. The Pico reads sensor data:
- Water level from **HC-SR04**
- Temperature from **DS18B20**
6. The Pico formats the data as an HTTP response: **Distance: XX cm
Temperature: XX.X C**
7. The ESP8266 sends the response back to the Flutter app.
8. The Flutter dashboard:
   - Displays live sensor readings
   - Updates system connection status
   - Stores values in history lists
   - Displays real-time **line graphs**

---

## Sensor Functionality

### Water Level Monitoring

The **HC-SR04 ultrasonic sensor** measures the distance between the sensor and the water surface.

- Smaller distance → higher water level
- Larger distance → lower water level

This value is displayed in the dashboard as **Water Level (cm)**.

---

### Temperature Monitoring

The **DS18B20 digital temperature sensor** measures water temperature.

Steps performed by the Pico:

1. Scan for connected sensors
2. Start temperature conversion
3. Wait for conversion
4. Read temperature value

The Flutter app displays this value as **Water Temperature (°C)**.

---

## Flutter Dashboard Features

### Real-Time Monitoring

The dashboard fetches data every **2 seconds** from the ESP8266 server.

---

### Sensor Cards

The UI shows three sensor panels:

- **Water Level**
- **pH Level** (currently static value)
- **Temperature**

Each card shows:

- Current value
- Status indicator
- Color-coded label

---

### Connection Indicator

The app displays a **connection status indicator** in the AppBar.

- 🟢 Connected → Data received successfully
- 🔴 Disconnected → HTTP request failed

---

### System Status

Displays pump status information for the aquaponics system.

Example: **pump on**


This can later be extended to include **pump control via HTTP commands**.

---

### Historical Data Graphs

The Flutter dashboard stores the **last 20 readings** and displays:

1. **Water Level History Graph**
2. **Temperature History Graph**

Graphs are drawn using **FL Chart** with smooth curved lines.

---

## Data Flow

Sensor Reading  
↓  
Raspberry Pi Pico  
↓ UART Communication  
ESP8266 HTTP Server  
↓ WiFi  
Flutter Desktop Dashboard  
↓  
Visualization & Graphs

---

## Future Improvements

Possible enhancements include:

- Real **pH sensor integration**
- **Automatic pump control**
- **Mobile Flutter app support**
- **Cloud database logging**
- **Remote monitoring via internet**
- **Notification alerts for abnormal conditions**

---

## References

1. https://www.youtube.com/watch?v=NkBL_VxJ77g

---

## Circuit,  Circuit Diagram and App Screenshots

<img width="739" height="513" alt="image" src="https://github.com/user-attachments/assets/c8de0bcd-29b6-445d-be32-abfefdba00f2" />

<img width="314" height="232" alt="image" src="https://github.com/user-attachments/assets/41ecc95d-5c84-4ba3-a7eb-eaba505ecb10" />

<img width="971" height="509" alt="image" src="https://github.com/user-attachments/assets/377fde95-a691-4958-b5db-395febc2d453" />

---

## Conclusion

This project demonstrates a complete **embedded IoT monitoring system** integrating:

- Raspberry Pi Pico microcontroller
- ESP8266 WiFi networking
- Sensor data acquisition
- UART-based microcontroller communication
- Flutter-based visualization dashboard

The system provides **real-time monitoring and graphical visualization of aquaponics parameters**, serving as a strong foundation for building advanced **smart farming and IoT-based environmental monitoring systems**.

---

# 11. Smart Fish Tank Pump Control System

**Author:** Nivedita Suresh, Nikhil H  

---

# Overview
---

A **wireless + automatic pump control system** built using **Raspberry Pi Pico, ESP8266, relay modules, and an ultrasonic sensor**.

The system automatically maintains the water level in a fish tank while allowing **manual wireless control through a web interface**.

This project is part of a **Smart Aquaponics / Fish Tank Monitoring System**.

---

# Features

- Automatic **water level monitoring**
- Automatic **pump activation**
- **Manual wireless enable/disable control**
- **Dual relay safety logic**
- Pump runs **only if manual relay is enabled**
- Real-time **web dashboard**
- Integration with:
  - DS18B20 temperature sensor
  - Servo fish feeder
  - ESP8266 WiFi module

---

# System Architecture

```
           WiFi Web Interface
                  │
                  │
               ESP8266
                  │ UART
                  │
          Raspberry Pi Pico
                  │
        ┌─────────┴─────────┐
        │                   │
 Ultrasonic Sensor     Pump Control
   (Water Level)            │
                            │
                     Manual Relay
                       (Enable)
                            │
                            │
                     Pump Relay
                       (Auto)
                            │
                            │
                          Pump
```

---

# Pump Control Logic

The system uses **two relays**:

1. **Manual Relay**
2. **Automatic Pump Relay**

The pump runs **only when both relays allow it**.

## Logic Flow

```
Manual Pump Enabled?
        │
        ├── NO → Pump OFF
        │
        └── YES
               │
        Water Level Low?
               │
         ├── NO → Pump OFF
         │
         └── YES → Pump ON
```

---

# Relay Logic Table

| Manual Relay | Pump Relay | Inlet Pump | Outlet Pump |
|---------------|-------------|-----------|--------------|
| OFF | Any | OFF | OFF |
| ON | OFF | OFF | ON |
| ON | ON | ON | ON |

---

# Hardware Components

| Component | Quantity |
|-----------|----------|
| Raspberry Pi Pico / Pico H | 1 |
| ESP8266 ESP-01 | 1 |
| Relay Module | 2 |
| Ultrasonic Sensor (HC-SR04) | 1 |
| DS18B20 Temperature Sensor | 1 |
| Servo Motor | 1 |
| 12V DC Water Pump | 1 |
| 12V Adapter | 1 |
| Flyback Diode (1N4007) | 1 |

---

# GPIO Connections

## Raspberry Pi Pico

| Device | Pico Pin |
|------|------|
| ESP8266 TX | GP1 |
| ESP8266 RX | GP0 |
| Ultrasonic Trigger | GP19 |
| Ultrasonic Echo | GP26 |
| DS18B20 Data | GP18 |
| Servo Motor | GP15 |
| Pump Relay | GP14 |
| Manual Relay | GP13 |

---

# Relay Module Connections

| Relay Pin | Connection |
|-----------|------------|
| VCC | 5V |
| GND | GND |
| IN | Pico GPIO |

---

# Pump Wiring

```
12V Adapter (+)
       │
       │
   COM (Manual Relay)
       │
       │
    NO
       │
       │
   COM (Pump Relay)
       │
       │
    NO
       │
     Pump +
Pump − ───────── Adapter −
```

---


# WiFi Configuration

The ESP8266 creates a **WiFi Access Point**.

```
SSID: Pico_Sensors
Password: 12345678
```

Open the dashboard at:

```
http://192.168.4.1
```

---

# Web Interface

The webpage displays:

- Water level
- Pump status
- Temperature
- pH placeholder
- Pump control buttons

Example display:

```
Fish Tank Status

Water Distance: 12 cm
Pump Status: Enabled - Waiting
Temperature: 27.4 °C
pH Level: 7.0

[ Enable Pump ]
[ Disable Pump ]
```

---

# Web Controls

| Button | Function |
|------|------|
| Enable Pump | Allows automatic pump operation |
| Disable Pump | Stops the pump completely |

---

# Software Stack

- MicroPython
- ESP8266 AT Firmware
- UART Communication
- HTTP Web Server
- Sensor Data Processing

---

# Future Improvements

- Mobile dashboard
- pH sensor integration
- Dissolved oxygen monitoring
- Water level alerts
- MQTT cloud monitoring
- Manual fish feeding from web interface

---


# Project Goal

To build a **smart aquaponics monitoring system** that automates fish tank management while allowing **remote monitoring and control**.
