from machine import UART, Pin, PWM
import time
import onewire
import ds18x20
import hcsr04

# ---------------- UART SETUP ----------------
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# ---------------- SENSOR SETUP ----------------
distance_sensor = hcsr04.HCSR04(trigger_pin=19, echo_pin=26)

dat = Pin(18)
ow = onewire.OneWire(dat)
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

print("DS18B20 Found:", roms)

# ---------------- SERVO SETUP ----------------
servo = PWM(Pin(15))
servo.freq(50)
servo.duty_u16(1500)

# ---------------- RELAY SETUP ----------------
relay_pump = Pin(14, Pin.OUT)      # pump relay (auto)
relay_enable = Pin(13, Pin.OUT)    # manual enable relay

manual_pump = True

# ---------------- FEEDING TIMER ----------------
FEEDING_INTERVAL = 8   # seconds (change to 8*60*60 for 8 hours)
last_feeding_time = time.time()

# ---------------- FISH FEED FUNCTION ----------------
def feed_fish():
    print("🐟 Feeding Fish...")

    servo.duty_u16(4900)
    time.sleep(1)

    servo.duty_u16(1500)
    time.sleep(1)

    print("Feeding Complete ✅")

# ---------------- ESP COMMAND FUNCTION ----------------
def send_at(cmd, delay=2):
    uart.write(cmd + "\r\n")
    time.sleep(delay)
    if uart.any():
        print(uart.read())

# ---------------- SETUP ESP8266 ----------------
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

    # -------- Fish Feeding Timer --------
    current_time = time.time()
    if current_time - last_feeding_time >= FEEDING_INTERVAL:
        feed_fish()
        last_feeding_time = current_time

    # -------- WATER DISTANCE --------
    try:
        distance = int(distance_sensor.distance_cm())
    except:
        distance = -1

    # -------- TEMPERATURE --------
    temperature = 0
    if len(roms) > 0:
        ds.convert_temp()
        time.sleep_ms(750)
        temperature = ds.read_temp(roms[0])

    # -------- PH PLACEHOLDER --------
    ph_value = 7.0

    # -------- RELAY CONTROL --------
    pump_status = "OFF"

    if manual_pump:
        relay_enable.value(1)

        if distance < 5 and distance != -1:
            relay_pump.value(1)
            pump_status = "ON (Auto Filling)"
        else:
            relay_pump.value(0)
            pump_status = "Enabled - Waiting"

    else:
        relay_enable.value(0)
        relay_pump.value(0)
        pump_status = "Disabled"

    # -------- ESP8266 REQUEST --------
    if uart.any():

        raw = uart.read()

        try:
            data = raw.decode("utf-8", "ignore")
        except:
            continue

        print("Received:", data)

        if "+IPD," in data:
            try:
                start = data.find("+IPD,") + 5
                link_id = data[start:start+1]

                # -------- BUTTON CONTROL --------
                if "/pump_on" in data:
                    manual_pump = True
                    print("Pump ENABLED")

                if "/pump_off" in data:
                    manual_pump = False
                    print("Pump DISABLED")

                # -------- WEB PAGE --------
                body = """
                <html>
                <head>
                <meta http-equiv="refresh" content="5">
                <title>Fish Tank Monitor</title>
                </head>
                <body>

                <h1>🐟 Fish Tank Status</h1>

                <p><b>Water Distance:</b> {} cm</p>
                <p><b>Pump Status:</b> {}</p>
                <p><b>Temperature:</b> {:.2f} °C</p>
                <p><b>pH Level:</b> {:.2f}</p>

                <br>

                <a href="/pump_on">
                <button style="font-size:20px;">Enable Pump</button>
                </a>

                <a href="/pump_off">
                <button style="font-size:20px;">Disable Pump</button>
                </a>

                </body>
                </html>
                """.format(distance, pump_status, temperature, ph_value)

                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "Content-Length: {}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "{}"
                ).format(len(body), body)

                uart.write("AT+CIPSEND={},{}\r\n".format(link_id, len(response)))
                time.sleep(1)

                uart.write(response)

                time.sleep(1)
                uart.write("AT+CIPCLOSE={}\r\n".format(link_id))

            except Exception as e:
                print("Error:", e)

    time.sleep(1)
