# Raspberry Pi Pico H

 The **Pico H** is the same as Pico but comes with **pre-soldered header pins** (which makes breadboard wiring easier for your aquaponics project).

Now I’ll give you a **clean, corrected, GitHub-ready detailed pinout + functions documentation** specifically titled for **Raspberry Pi Pico H**.

You can directly copy-paste this into your GitHub.

---

# Raspberry Pi Pico H – Detailed Pinout and Functional Datasheet

---

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

---

# 2. Complete Pinout Diagram (40-Pin Layout)

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
```

---

# 3. Power Pins (Detailed Explanation)

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

---

# 4. GPIO Pins (GP0 – GP28)

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

---

# 5. Analog Input Pins (ADC)

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

---

# 6. PWM Capability

PWM available on almost all GPIO pins.

Used for:

* Servo motor control (fish feeder)
* Pump speed control
* Aerator control

Example recommended pins:

* GP15 → Servo
* GP14 → Pump Relay

---

# 7. Communication Interfaces

## UART

| UART  | TX  | RX  |
| ----- | --- | --- |
| UART0 | GP0 | GP1 |
| UART1 | GP4 | GP5 |

Used for:

* Serial debugging
* GPS module
* Communication modules

---

## I2C

| I2C  | SDA | SCL |
| ---- | --- | --- |
| I2C0 | GP0 | GP1 |
| I2C1 | GP2 | GP3 |

Used for:

* RTC Module (DS3231)
* LCD Display
* Digital environmental sensors

---

## SPI

| SPI  | Pins      |
| ---- | --------- |
| SPI0 | GP16–GP19 |
| SPI1 | GP10–GP13 |

Used for:

* SD card module
* TFT displays

---

# 8. Special Function Pins

| Pin      | Function                  |
| -------- | ------------------------- |
| RUN      | Reset pin                 |
| ADC_VREF | External analog reference |
| 3V3_EN   | Power control             |
| AGND     | Analog ground             |

---

# 9. Internal Temperature Sensor

* Connected to ADC4
* Measures RP2040 chip temperature
* Useful for enclosure heat monitoring

---

# 10. Recommended Pin Allocation for Your Smart Aquaponics System

| Component          | Suggested GPIO |
| ------------------ | -------------- |
| pH Sensor          | GP26           |
| Ammonia Sensor     | GP27           |
| Temperature Sensor | GP28           |
| Servo Motor        | GP15           |
| Relay Module       | GP14           |
| RTC (I2C)          | GP0, GP1       |
| LCD Display        | GP2, GP3       |

---

# 11. Design Precautions

* Never apply 5V directly to GPIO
* Use relay or transistor for pumps
* Use common ground for all modules
* Use voltage divider for high-voltage sensors
* Provide proper decoupling capacitors

---

