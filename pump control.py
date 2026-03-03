from machine import Pin
import time

# Relay connected to GP15
relay = Pin(15, Pin.OUT)

print("Smart Aquaponics Pump Control Started")

while True:
    print("Pump ON - Water Circulation Started")
    relay.value(1)   # Turn relay ON
    time.sleep(5)    # Pump runs for 5 seconds
    
    print("Pump OFF - Water Circulation Stopped")
    relay.value(0)   # Turn relay OFF
    time.sleep(5)    # Wait for 5 seconds
