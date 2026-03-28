from machine import UART, Pin, PWM, ADC
import time
import onewire
import ds18x20
import hcsr04

# ---------------- UART SETUP ----------------
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# ---------------- SENSOR SETUP ----------------
distance_sensor = hcsr04.HCSR04(trigger_pin=19, echo_pin=26)

# DS18B20
dat = Pin(18)
ow = onewire.OneWire(dat)
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

print("DS18B20 Found:", roms)

# ---------------- PH SENSOR ----------------
ph_sensor = ADC(27)   # GP27 (ADC1)

def read_ph():
    total = 0
    for _ in range(10):  # averaging for stability
        total += ph_sensor.read_u16()
        time.sleep(0.01)

    avg = total / 10
    voltage = avg * 3.3 / 65535

    ph = ((2.5 - voltage) / 0.18)

    return ph

# ---------------- SERVO ----------------
servo = PWM(Pin(15))
servo.freq(50)
servo.duty_u16(1500)

# ---------------- RELAY ----------------
relay_pump = Pin(14, Pin.OUT)
relay_enable = Pin(13, Pin.OUT)

manual_pump = True
esp_busy = False

# ---------------- SENSOR STORAGE ----------------
latest_distance = 0
latest_temperature = 0
ph_value = 7.0

# ---------------- FEED TIMER ----------------
FEEDING_INTERVAL = 20
last_feeding_time = time.time()

# ---------------- FEED FUNCTION ----------------
def feed_fish():
    print("🐟 Feeding Fish...")
    servo.duty_u16(4900)
    time.sleep(1)
    servo.duty_u16(1500)
    time.sleep(1)
    print("Feeding Complete ✅")

# ---------------- ESP COMMAND ----------------
def send_at(cmd, delay=2):
    uart.write(cmd + "\r\n")
    time.sleep(delay)
    if uart.any():
        print(uart.read())

# ---------------- SETUP ESP ----------------
send_at("AT+RST", 3)
send_at("AT+CWMODE=2")
send_at('AT+CWSAP="Pico_Sensors","12345678",5,3')
send_at("AT+CIPMUX=1")
send_at("AT+CIPSERVER=1,80")

print("Server Ready")
print("Connect WiFi: Pico_Sensors")
print("Open: http://192.168.4.1")

# ---------------- MAIN LOOP ----------------
while True:

    # ========= 1. HANDLE WEB =========
    if uart.any():
        raw = uart.read()

        try:
            data = raw.decode("utf-8", "ignore")
        except:
            continue

        print("Web Request Received")
        print("RAW DATA:\n", data)

        if "+IPD," in data:
            try:
                esp_busy = True

                start = data.find("+IPD,") + 5
                link_id = data[start]

                if "/pump_on" in data:
                    manual_pump = True
                    print("Pump Enabled from Web")

                if "/pump_off" in data:
                    manual_pump = False
                    print("Pump Disabled from Web")

                body = """<h2>🐟 Fish Tank</h2>

Distance: {} cm<br>
Pump: {}<br>
Temp: {:.2f} C<br>
pH: {:.2f}<br><br>
<a href="/pump_on">Enable Pump</a><br>
<a href="/pump_off">Disable Pump</a>
""".format(
                    latest_distance,
                    "ON (Auto)" if manual_pump else "Disabled",
                    latest_temperature,
                    ph_value
                )

                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "{}"
                ).format(body)

                uart.write("AT+CIPSEND={},{}\r\n".format(link_id, len(response)))
                time.sleep(0.5)

                uart.write(response)
                time.sleep(1)

                uart.write("AT+CIPCLOSE={}\r\n".format(link_id))

                esp_busy = False

            except Exception as e:
                print("Error:", e)
                esp_busy = False

    # ========= 2. SENSOR UPDATE =========
    try:
        latest_distance = int(distance_sensor.distance_cm())
    except:
        latest_distance = -1

    if len(roms) > 0:
        ds.convert_temp()
        time.sleep_ms(100)
        try:
            latest_temperature = ds.read_temp(roms[0])
        except:
            pass

    ph_value = read_ph()

    print("Distance:", latest_distance, "cm")
    print("Temperature:", round(latest_temperature, 2), "C")
    print("pH Value:", round(ph_value, 2))

    # ========= 3. FEEDING =========
    current_time = time.time()
    if current_time - last_feeding_time >= FEEDING_INTERVAL and not esp_busy:
        feed_fish()
        last_feeding_time = current_time

    # ========= 4. RELAY CONTROL =========
    if manual_pump:
        relay_enable.value(1)
        print("Pump Mode: AUTO")

        if latest_distance < 5 and latest_distance != -1:
            relay_pump.value(1)
            print("Pump: ON (Water LOW)")
        else:
            relay_pump.value(0)
            print("Pump: OFF (Water OK)")
    else:
        relay_enable.value(0)
        relay_pump.value(0)
        print("Pump Mode: MANUAL OFF")

    print("------ SYSTEM STATUS ------")
    print("Distance:", latest_distance)
    print("Temperature:", round(latest_temperature, 2))
    print("pH:", round(ph_value, 2))
    print("---------------------------")

    time.sleep(0.5) 
