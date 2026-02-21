import machine
import onewire, ds18x20
import time
from machine import Pin, PWM, time_pulse_us

# ==============================
# --- Hardware Setup ---
# ==============================

# DS18B20 on GP22
ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
print('Found DS18B20 devices:', roms)

# Ultrasonic pins
trig = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

# Alert LED
alert_led = Pin(14, Pin.OUT)

# Servo setup (Fish Feeder)
servo = PWM(Pin(15))
servo.freq(50)

# ==============================
# --- Configuration ---
# ==============================

TEMP_HIGH = 35.0
TEMP_LOW = 30.0

DIST_MIN = 5
DIST_MAX = 10

FEEDING_INTERVAL = 8  # 8 hours
last_feeding_time = time.time()


# ==============================
# --- Distance Function ---
# ==============================

def get_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()

    duration = time_pulse_us(echo, 1, 30000)

    if duration <= 0:
        return None

    distance = (duration * 0.0343) / 2
    return round(distance, 2)

# ==============================
# --- Fish Feeding Function ---
# ==============================

def feed_fish():
    print("🐟 Feeding Fish...")

    # Rotate to ~90°
    servo.duty_u16(4900)
    time.sleep(1)

    # Return to ~0°
    servo.duty_u16(1500)
    time.sleep(1)

    print("Feeding Complete ✅")

# ==============================
# --- Main Loop ---
# ==============================

while True:

    temp_alert = False
    dist_alert = False

    # -------- Temperature --------
    if roms:
        ds_sensor.convert_temp()
        time.sleep_ms(750)

        for rom in roms:
            temp = round(ds_sensor.read_temp(rom), 2)

            if temp >= TEMP_HIGH:
                temp_alert = True
                temp_status = "[TEMPERATURE HIGH!]"
            elif temp <= TEMP_LOW:
                temp_alert = True
                temp_status = "[TEMPERATURE LOW!]"
            else:
                temp_status = "[IDEAL TEMPERATURE]"

            print(f"Water Temp: {temp}°C {temp_status}")
    else:
        temp_alert = True
        print("Temperature sensor missing!")

    # -------- Distance --------
    dist = get_distance()

    if dist is None:
        print("WATER LEVEL: Sensor error")
        dist_alert = True
    else:
        if DIST_MIN <= dist <= DIST_MAX:
            dist_status = "[WATER LEVEL IS IDEAL]"
        elif DIST_MIN >= dist:
           dist_status = "[WATER LEVEL IS LOW]" 
        else:
            dist_status = "[WATER LEVEL IS HIGH!]"
            dist_alert = True

        print(f"WATER LEVEL: {dist} cm {dist_status}")

    # -------- LED Alert Logic --------
    alert_led.value(temp_alert or dist_alert)

    # -------- Fish Feeding Timer --------
    current_time = time.time()
    if current_time - last_feeding_time >= FEEDING_INTERVAL:
        feed_fish()
        last_feeding_time = current_time
        print("Next feeding in 8 hours...")

    print("-----------------------------")
    time.sleep(1)
