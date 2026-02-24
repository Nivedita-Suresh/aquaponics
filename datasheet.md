# Raspberry Pi Pico H – Detailed Pinout and Functional Datasheet

## 1. Overview

The Raspberry Pi Pico H is a microcontroller development board based on the RP2040 chip. It features:

* Dual-core ARM Cortex-M0+ processor
* 133 MHz clock speed
* 264 KB SRAM
* 2 MB Flash
* 26 multifunction GPIO pins
* 3 ADC inputs
* PWM on most GPIO
* UART, SPI, I2C support
* Pre-soldered 40-pin headers

Operating Logic Level: **3.3V (Not 5V tolerant)**

## 2. Complete Pinout Diagram (40-Pin Layout)

```
          ┌──────────────────────────┐
 GP0   1  │•                         │ 40  VBUS
 GP1   2  │                          │ 39  VSYS
 GND   3  │                          │ 38  GND
 GP2   4  │                          │ 37  3V3_EN
 GP3   5  │                          │ 36  3V3(OUT)
 GP4   6  │                          │ 35  ADC_VREF
 GP5   7  │                          │ 34  GP28 / ADC2
 GND   8  │                          │ 33  AGND
 GP6   9  │                          │ 32  GP27 / ADC1
 GP7  10  │                          │ 31  GP26 / ADC0
 GP8  11  │                          │ 30  RUN
 GP9  12  │                          │ 29  GP22
 GND  13  │                          │ 28  GND
 GP10 14  │                          │ 27  GP21
 GP11 15  │                          │ 26  GP20
 GP12 16  │                          │ 25  GP19
 GP13 17  │                          │ 24  GP18
 GND  18  │                          │ 23  GND
 GP14 19  │                          │ 22  GP17
 GP15 20  │                          │ 21  GP16
          └──────────────────────────┘

## 3. Power Pins (Detailed Explanation)

| Pin      | Function         | Description         | Usage in Aquaponics         |
| -------- | ---------------- | ------------------- | --------------------------- |
| VBUS     | 5V from USB      | Direct USB supply   | Powering board via USB      |
| VSYS     | External Supply  | 1.8V – 5.5V input   | Battery/adapter input       |
| 3V3(OUT) | Regulated 3.3V   | Max ~300mA output   | Power sensors               |
| 3V3_EN   | Regulator Enable | LOW disables 3.3V   | Rarely used                 |
| GND      | Ground           | Circuit reference   | Must connect to all modules |
| AGND     | Analog Ground    | Clean ADC reference | For analog sensors          |
| ADC_VREF | ADC Reference    | External analog ref | Optional precision ADC      |

 Important: GPIO pins operate at **3.3V only**.

## 4. GPIO Pins (GP0 – GP28)

Total usable GPIO pins: **26**

Each GPIO can act as:

* Digital Input
* Digital Output
* PWM Output
* UART
* I2C
* SPI
* PIO (Programmable I/O)

Max current per GPIO: **12 mA**
Total combined GPIO current: **50 mA**

## 5. Analog Input Pins (ADC)

| GPIO     | ADC Channel | Use in Aquaponics             |
| -------- | ----------- | ----------------------------- |
| GP26     | ADC0        | pH Sensor                     |
| GP27     | ADC1        | Ammonia Sensor                |
| GP28     | ADC2        | Water Level Sensor            |
| Internal | ADC4        | Temperature sensor (internal) |

ADC Resolution: **12-bit**

Best practice:

* Connect sensor GND to AGND
* Use stable voltage reference

## 6. PWM Capability

PWM available on almost all GPIO pins.

Used for:

* Servo motor control (fish feeder)
* Pump speed control
* Aerator control

Example recommended pins:

* GP15 → Servo
* GP14 → Pump Relay

## 7. Communication Interfaces

## UART

| UART  | TX  | RX  |
| ----- | --- | --- |
| UART0 | GP0 | GP1 |
| UART1 | GP4 | GP5 |

Used for:

* Serial debugging
* GPS module
* Communication modules


## I2C

| I2C  | SDA | SCL |
| ---- | --- | --- |
| I2C0 | GP0 | GP1 |
| I2C1 | GP2 | GP3 |

Used for:

* RTC Module (DS3231)
* LCD Display
* Digital environmental sensors

## SPI

| SPI  | Pins      |
| ---- | --------- |
| SPI0 | GP16–GP19 |
| SPI1 | GP10–GP13 |

Used for:

* SD card module
* TFT displays


## 8. Special Function Pins

| Pin      | Function                  |
| -------- | ------------------------- |
| RUN      | Reset pin                 |
| ADC_VREF | External analog reference |
| 3V3_EN   | Power control             |
| AGND     | Analog ground             |


## 9. Internal Temperature Sensor

* Connected to ADC4
* Measures RP2040 chip temperature
* Useful for enclosure heat monitoring


## 10. Recommended Pin Allocation for Your Smart Aquaponics System

| Component          | Suggested GPIO |
| ------------------ | -------------- |
| pH Sensor          | GP26           |
| Ammonia Sensor     | GP27           |
| Temperature Sensor | GP28           |
| Servo Motor        | GP15           |
| Relay Module       | GP14           |
| RTC (I2C)          | GP0, GP1       |
| LCD Display        | GP2, GP3       |


## 11. Design Precautions

* Never apply 5V directly to GPIO
* Use relay or transistor for pumps
* Use common ground for all modules
* Use voltage divider for high-voltage sensors
* Provide proper decoupling capacitors

## 1️ Water Level Monitoring Sensor Datasheet

# Water Level Monitoring Sensor 

## 1. Overview

The Water Level Sensor is used to detect and measure the water level in a tank or grow bed. It works on the principle of varying resistance based on water contact.

In a Smart Aquaponics System, it helps:

* Monitor fish tank water level
* Prevent dry run of water pump
* Detect overflow conditions

## 2. Operating Principle

* The sensor contains parallel exposed conductive traces.
* When water touches the traces, resistance decreases.
* The output voltage changes accordingly.
* The microcontroller reads this as an analog signal.

## 3. Technical Specifications

| Parameter           | Value         |
| ------------------- | ------------- |
| Operating Voltage   | 3.3V – 5V     |
| Output Type         | Analog        |
| Current Consumption | <20mA         |
| Working Temperature | 0°C – 50°C    |
| Detection Type      | Contact-based |

## 4. Pin Configuration

| Pin | Function                        |
| --- | ------------------------------- |
| VCC | Power supply (3.3V recommended) |
| GND | Ground                          |
| A0  | Analog Output                   |

## 5. Interfacing with Raspberry Pi Pico H

| Sensor Pin | Pico Pin    |
| ---------- | ----------- |
| VCC        | 3V3(OUT)    |
| GND        | AGND        |
| A0         | GP28 (ADC2) |

## 6. Application in Aquaponics

* Monitor sump tank water level
* Auto control pump
* Alert during low water condition

## 7. Limitations

* Prone to corrosion over time
* Not suitable for long-term submerged use
* Accuracy depends on water conductivity

## 2️ Temperature Sensor 

## 1. Overview

The DS18B20 is a digital temperature sensor using the 1-Wire protocol. It provides high accuracy and is waterproof (probe type).

Ideal for:

* Fish tank temperature monitoring
* Grow bed temperature monitoring

## 2. Technical Specifications

| Parameter         | Value                  |
| ----------------- | ---------------------- |
| Operating Voltage | 3.0V – 5.5V            |
| Temperature Range | -55°C to +125°C        |
| Accuracy          | ±0.5°C (-10°C to 85°C) |
| Interface         | 1-Wire Digital         |
| Resolution        | 9–12 bit               |

## 3. Pin Configuration

| Pin  | Function       |
| ---- | -------------- |
| VCC  | 3.3V           |
| GND  | Ground         |
| DATA | Digital signal |

⚠️ Requires 4.7kΩ pull-up resistor between DATA and VCC.

## 4. Interfacing with Raspberry Pi Pico H

| Sensor Pin | Pico Pin |
| ---------- | -------- |
| VCC        | 3V3(OUT) |
| GND        | GND      |
| DATA       | GP16     |

## 5. Advantages

* Waterproof probe
* High accuracy
* No analog noise
* Long cable support

## 3️ Servo Motor 

# SG90 Servo Motor 

## 1. Overview

The SG90 is a small PWM-controlled servo motor used for controlled angular movement (0°–180°).

Used in aquaponics for:

* Automatic fish feeder
* Valve control

## 2. Technical Specifications

| Parameter         | Value     |
| ----------------- | --------- |
| Operating Voltage | 4.8V – 6V |
| Stall Torque      | 1.8 kg·cm |
| Operating Speed   | 0.1s/60°  |
| Rotation Angle    | 0°–180°   |
| Control Signal    | PWM       |

## 3. Pin Configuration

| Wire Color | Function   |
| ---------- | ---------- |
| Brown      | GND        |
| Red        | 5V         |
| Orange     | PWM Signal |

## 4. Interfacing with Raspberry Pi Pico H

| Servo Wire | Pico Connection     |
| ---------- | ------------------- |
| Red        | External 5V supply  |
| Brown      | GND (Common Ground) |
| Orange     | GP15 (PWM)          |

 Do NOT power servo from Pico 3.3V.


## 4️ pH Sensor

## 1. Overview

The pH Sensor Module measures acidity or alkalinity of water.

In aquaponics:

* Ideal pH range: 6.5 – 7.5
* Critical for fish and plant health


## 2. Working Principle

* Glass electrode generates voltage based on hydrogen ion concentration.
* Signal conditioning board amplifies small millivolt signal.
* Outputs analog voltage to microcontroller.


## 3. Technical Specifications

| Parameter         | Value     |
| ----------------- | --------- |
| Operating Voltage | 5V        |
| Output Type       | Analog    |
| Measuring Range   | 0 – 14 pH |
| Accuracy          | ±0.1 pH   |
| Response Time     | <1 minute |


## 4. Pin Configuration

| Pin | Function                  |
| --- | ------------------------- |
| VCC | 5V                        |
| GND | Ground                    |
| AO  | Analog Output             |
| DO  | Digital Output (optional) |


## 5. Interfacing with Raspberry Pi Pico H

| Sensor Pin | Pico Pin    |
| ---------- | ----------- |
| VCC        | External 5V |
| GND        | AGND        |
| AO         | GP26 (ADC0) |

⚠️ Ensure output does not exceed 3.3V (use voltage divider if required).


## 6. Importance in Aquaponics

* Maintains nutrient availability
* Prevents fish stress
* Controls ammonia toxicity






