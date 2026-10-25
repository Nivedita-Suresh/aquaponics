from machine import Pin, PWM, SPI
import time
import onewire
import ds18x20
import hcsr04
from sx1278 import SX1278

# ---------------- LORA SETUP ----------------
spi = SPI(0, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))
lora = SX1278(spi, cs=5, rst=6, freq=433E6)
lora.listen()
print("LoRa Ready")

# ---------------- SENSOR SETUP ----------------
distance_sensor = hcsr04.HCSR04(trigger_pin=19, echo_pin=26)

ow = onewire.OneWire(Pin(18))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
print("DS18B20 Found:", roms)

# ---------------- SERVO SETUP ----------------
servo = PWM(Pin(15))
servo.freq(50)
servo.duty_u16(1500)

# ---------------- RELAY SETUP ----------------
relay_pump = Pin(14, Pin.OUT)
relay_enable = Pin(13, Pin.OUT)
manual_pump = True

# ---------------- FEEDING TIMER ----------------
FEEDING_INTERVAL = 8          # seconds (use 8*60*60 for 8 hours)
last_feeding_time = time.time()

def feed_fish():
    print("Feeding Fish...")
    servo.duty_u16(4900)
    time.sleep(1)
    servo.duty_u16(1500)
    time.sleep(1)
    print("Feeding Complete")

# ---------------- TIMING ----------------
SEND_INTERVAL_MS = 5000
last_send = time.ticks_ms()
temp_started = False
temp_start_ms = 0
temperature = 0
ph_value = 7.0

while True:
    # -------- Feeding timer --------
    now = time.time()
    if now - last_feeding_time >= FEEDING_INTERVAL:
        feed_fish()
        last_feeding_time = now

    # -------- Distance --------
    try:
        distance = int(distance_sensor.distance_cm())
    except:
        distance = -1

    # -------- Temperature (non-blocking) --------
    if roms:
        if not temp_started:
            ds.convert_temp()
            temp_start_ms = time.ticks_ms()
            temp_started = True
        elif time.ticks_diff(time.ticks_ms(), temp_start_ms) >= 750:
            temperature = ds.read_temp(roms[0])
            temp_started = False

    # -------- Relay control --------
    if manual_pump:
        relay_enable.value(1)
        if distance != -1 and distance < 5:
            relay_pump.value(1)
            pump_status = "ON"
        else:
            relay_pump.value(0)
            pump_status = "WAIT"
    else:
        relay_enable.value(0)
        relay_pump.value(0)
        pump_status = "OFF"

    # -------- Receive commands --------
    msg = lora.receive()
    if msg:
        print("Received:", msg)
        if msg == "PUMP_ON":
            manual_pump = True
        elif msg == "PUMP_OFF":
            manual_pump = False

    # -------- Send data --------
    if time.ticks_diff(time.ticks_ms(), last_send) >= SEND_INTERVAL_MS:
        packet = "{},{:.2f},{:.2f},{}".format(distance, temperature, ph_value, pump_status)
        lora.send(packet)       # leaves radio in standby
        lora.listen()           # back to RX for commands
        print("Sent:", packet)
        last_send = time.ticks_ms()

    time.sleep_ms(100)
