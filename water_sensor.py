import machine
import rp2
import sys
import utime 

water_level_sensor = machine.ADC(26)

def read_water_level():

    while True:
        value = water_level_sensor.read_u16()
        print("A0: " ,value)
        utime.sleep_ms(400)


if __name__ == "__main__":
    water = read_water_level()
    if water is not None:
        print(f"Water level: {water} ")
    else:
        print("Failed to read valid sensor data.")
