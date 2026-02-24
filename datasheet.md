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



---

# 4. Pin Classification and Functions

---

## 4.1 Power Pins

| Pin      | Function      | Description                        |
| -------- | ------------- | ---------------------------------- |
| VBUS     | 5V Input      | Directly from USB                  |
| VSYS     | System Input  | 1.8V–5.5V external supply          |
| 3V3(OUT) | 3.3V Output   | Regulated output (max ~300mA)      |
| 3V3_EN   | Enable Pin    | Pull LOW to disable 3.3V regulator |
| GND      | Ground        | Common ground reference            |
| AGND     | Analog Ground | Used for ADC stability             |

---

## 4.2 Digital GPIO Pins (GP0 – GP28)

Total: **26 usable GPIO pins**

Each GPIO pin can function as:

* Digital Input
* Digital Output
* PWM Output
* UART
* SPI
* I2C
* PIO (Programmable I/O)

All GPIO operate at **3.3V logic level**
⚠️ Not 5V tolerant.

---

## 4.3 ADC Pins (Analog Inputs)

| GPIO     | ADC Channel               |
| -------- | ------------------------- |
| GP26     | ADC0                      |
| GP27     | ADC1                      |
| GP28     | ADC2                      |
| Internal | ADC4 (Temperature Sensor) |

Resolution: **12-bit ADC**

Used in aquaponics for:

* pH sensor (via signal conditioning)
* Ammonia sensor
* Water level analog sensor

---

## 4.4 PWM Capability

Almost all GPIO pins support PWM.

Used for:

* Servo motor control
* Pump speed control
* Aerator control

---

## 4.5 Communication Interfaces

### UART

* UART0 → GP0 (TX), GP1 (RX)
* UART1 → GP4 (TX), GP5 (RX)

Used for:

* GPS module
* Serial debugging
* WiFi modules

---

### I2C

* I2C0 → GP0, GP1
* I2C1 → GP2, GP3

Used for:

* RTC module
* LCD display
* Digital sensors

---

### SPI

* SPI0 → GP16–GP19
* SPI1 → GP10–GP13

Used for:

* Display modules
* SD card module

---

## 4.6 Special Pins

| Pin      | Function                       |
| -------- | ------------------------------ |
| RUN      | Reset pin                      |
| ADC_VREF | External ADC reference voltage |

---

# 5. Internal Temperature Sensor

Built-in temperature sensor connected to ADC4.
Useful for monitoring controller temperature inside enclosure.

---

# 6. Electrical Characteristics

| Parameter            | Value |
| -------------------- | ----- |
| GPIO Voltage         | 3.3V  |
| Max Current per GPIO | 12 mA |
| Total GPIO Current   | 50 mA |
| Flash Size           | 2MB   |

---

# 7. Recommended Pin Usage in Smart Aquaponics

| Function           | Recommended GPIO |
| ------------------ | ---------------- |
| pH Sensor          | GP26 (ADC0)      |
| Ammonia Sensor     | GP27 (ADC1)      |
| Temperature Sensor | GP28 (ADC2)      |
| Servo Motor        | GP15 (PWM)       |
| Water Pump Relay   | GP14             |
| RTC Module         | GP0, GP1 (I2C)   |
| LCD Display        | GP2, GP3 (I2C)   |

---

# 8. Important Design Considerations

* Use voltage divider if sensor output >3.3V
* Always connect common ground
* Use external ADC conditioning for pH sensor
* Do not power 5V devices directly from GPIO
* Use transistor or relay for pump control

---

# 9. Why Raspberry Pi Pico H is Suitable for Aquaponics

* Low power consumption
* High processing speed
* Multiple ADC inputs
* Multiple communication protocols
* Stable 3.3V regulator
* Affordable

---


