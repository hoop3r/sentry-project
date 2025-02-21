from machine import Pin
import time

pir_sensor = Pin(0, Pin.IN)

while True:

    if pir_sensor.value() == 0:
        print("Monitoring...")
    else:
        print("Somebody here!")

    time.sleep(0.1)