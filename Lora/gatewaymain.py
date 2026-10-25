from machine import Pin, SPI
import time
from sx1278 import SX1278

spi = SPI(0, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))
lora = SX1278(spi, cs=5, rst=6, freq=433E6)
lora.listen()

btn_on = Pin(14, Pin.IN, Pin.PULL_UP)
btn_off = Pin(15, Pin.IN, Pin.PULL_UP)

def send_cmd(cmd):
    lora.send(cmd)
    lora.listen()
    print("Command sent:", cmd)

print("Receiver ready")

while True:
    msg = lora.receive()
    if msg:
        try:
            d, t, ph, pump = msg.split(",")
            print("-" * 30)
            print("Water distance:", d, "cm")
            print("Temperature   :", t, "C")
            print("pH            :", ph)
            print("Pump          :", pump)
        except:
            print("Bad packet:", msg)

    if btn_on.value() == 0:
        send_cmd("PUMP_ON");  time.sleep_ms(400)
    if btn_off.value() == 0:
        send_cmd("PUMP_OFF"); time.sleep_ms(400)

    time.sleep_ms(50)
