# LoRa Link (SX1278): Fish Tank Monitor

This document covers only the LoRa communication part of the project. It replaces the original ESP8266 WiFi link between the tank node and the user.

## Overview

Two nodes communicate over a point-to-point LoRa link (no LoRaWAN, no internet):

```
 Tank node (Raspberry Pi Pico + SX1278)            Gateway (ESP32 + SX1278)
   sensors, pump relays, feeder                     web page for the dashboard app
            │                                                  │
            │ ── data packet every 5 s ───────────────────►    │
            │ ◄─────────── PUMP_ON / PUMP_OFF ────────────     │
            │            LoRa 433 MHz, SF7, 125 kHz            │
                                                               ▼
                                                    WiFi (HTTP) → Flutter app
```

- **Tank node:** reads the sensors and transmits a data packet every 5 seconds, then listens for pump commands.
- **Gateway:** receives the packets, keeps the latest values and serves them over WiFi. Pump buttons on its page send commands back over LoRa.

## Hardware

| Part | Node |
|---|---|
| Raspberry Pi Pico | Tank node |
| SX1278 LoRa module (433 MHz) + antenna | Tank node and gateway |
| ESP32 | Gateway |

**Note:** the SX1278 is a 3.3 V device. Never connect it to 5 V, and always attach the antenna before powering on.

## Wiring

**SX1278 to Pico (SPI0), tank node**

| SX1278 | Pico |
|---|---|
| 3.3V | 3V3 |
| GND | GND |
| SCK | GP2 |
| MOSI | GP3 |
| MISO | GP4 |
| NSS / CS | GP5 |
| RST | GP6 |

**SX1278 to ESP32, gateway**

| SX1278 | ESP32 |
|---|---|
| 3.3V | 3V3 |
| GND | GND |
| SCK | GPIO18 |
| MOSI | GPIO23 |
| MISO | GPIO19 |
| NSS / CS | GPIO5 |
| RST | GPIO14 |

The DIO pins are not used. The driver polls the status registers instead.

## Software

| File | Runs on | Purpose |
|---|---|---|
| `sx1278.py` | Both nodes | Minimal MicroPython SX1278 driver (init, send, listen, receive) |
| `main.py` (tank) | Pico | Sensors, relays, feeder, LoRa transmit/receive |
| `main.py` (gateway) | ESP32 | LoRa receive, WiFi access point, web page, command forwarding |

The same `sx1278.py` is used on both nodes, which keeps the radio settings identical.

### Driver API

```python
from machine import Pin, SPI
from sx1278 import SX1278

spi = SPI(0, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))      # Pico pins
lora = SX1278(spi, cs=5, rst=6, freq=433E6)

lora.send("hello")        # transmit a string, then return to standby
lora.listen()             # switch to continuous receive
msg = lora.receive()      # returns a string, or None if nothing arrived
```

On the ESP32, use `SPI(1, ...)` with pins 18/23/19, `cs=5` and `rst=14`.

## Radio Settings

| Parameter | Value | Reason |
|---|---|---|
| Frequency | 433 MHz | The SX1278 is a 433 MHz chip, in a license-free ISM band |
| Spreading factor | SF7 | Shortest airtime and lowest power. Enough range for a nearby tank |
| Bandwidth | 125 kHz | Standard value, a good balance of sensitivity and speed |
| Coding rate | 4/5 | Lowest overhead. Packets are tiny and the link is short |
| TX power | 17 dBm (PA_BOOST) | Good range without the full 20 dBm current draw |
| Sync word | 0x12 | Private network ID, ignores other LoRa traffic |
| CRC | Enabled | Corrupted packets are discarded |
| Header | Explicit | Packet carries its own length |
| Preamble | 8 symbols | Standard length for reliable synchronisation |
| LNA boost / AGC | On | Better receive sensitivity, automatic gain |
| SPI speed | 1 MHz | Safe for jumper-wire connections |

**Both nodes must use identical frequency, SF, bandwidth, coding rate and sync word, or no packets will be received.**

Derived values for these settings:
- Bit rate ≈ 5.47 kbps
- Airtime of an 18-byte packet ≈ 46 ms
- Duty cycle at one packet per 5 s ≈ 0.9%

## Message Format

**Tank node to gateway** (plain text, comma-separated):

```
distance,temperature,pH,pump_status
```

Example: `12,24.50,7.00,WAIT`

| Field | Meaning |
|---|---|
| distance | Water distance in cm from the HC-SR04 (`-1` if the reading failed) |
| temperature | Water temperature in °C from the DS18B20 |
| pH | pH value (currently a fixed placeholder, 7.0) |
| pump_status | `ON`, `WAIT` or `OFF` |

**Gateway to tank node** (commands):

| Command | Effect |
|---|---|
| `PUMP_ON` | Enables the pump (automatic filling when the water is low) |
| `PUMP_OFF` | Disables the pump |

The gateway sends each command twice to improve the chance it is received.

## How It Works

1. The tank node reads the sensors and builds the text packet.
2. The packet is written into the SX1278 FIFO over SPI and transmitted.
3. The tank node switches back to receive mode to wait for commands.
4. The gateway's SX1278 demodulates the packet, checks the CRC and stores the payload.
5. The gateway parses the values and updates its web page.
6. When a pump button is pressed, the gateway transmits `PUMP_ON` or `PUMP_OFF`.
7. The tank node applies the command, and the new pump state appears in the next packet.

If the gateway receives nothing for 20 seconds, it shows the link as **OFFLINE**.

## Setup

1. Wire the SX1278 modules as shown above, with antennas attached.
2. Copy `sx1278.py` to both the Pico and the ESP32.
3. Copy the tank `main.py` to the Pico and the gateway `main.py` to the ESP32.
4. Power both boards. The tank node prints `LoRa Ready` and `Sent: ...` every 5 seconds. The gateway prints `Received: ...`.
5. Connect to the gateway's WiFi network and open `http://192.168.4.1`.
