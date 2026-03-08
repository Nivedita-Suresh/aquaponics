from machine import UART, Pin
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

# ---------------- ESP COMMAND FUNCTION ----------------
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
                link_id = data[start]

                # -------- SENSOR READ --------
                try:
                    distance = int(distance_sensor.distance_cm())
                except:
                    distance = -1

                temperature = 0

                if len(roms) > 0:
                    ds.convert_temp()
                    time.sleep_ms(750)
                    temperature = ds.read_temp(roms[0])

                # -------- RESPONSE BODY --------
                body = "Distance: {} cm\nTemperature: {:.2f} C".format(distance, temperature)

                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: {}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "{}"
                ).format(len(body), body)

                uart.write("AT+CIPSEND={},{}\r\n".format(link_id, len(response)))
                time.sleep(0.5)
                uart.write(response)

                time.sleep(0.5)
                uart.write("AT+CIPCLOSE={}\r\n".format(link_id))

            except Exception as e:
                print("Error:", e)

    time.sleep(0.1)
