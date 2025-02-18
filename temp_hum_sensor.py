from machine import Pin, I2C
import time

I2C_INTERFACE = 0
SDA_PIN = Pin(16)
SCL_PIN = Pin(17)

i2c = I2C(I2C_INTERFACE, scl=SCL_PIN, sda=SDA_PIN, freq=100000)

SHT30_ADDRESS = 0x44

MEASURE_CMD = b'\x2C\x06'

def read_temperature_humidity():
    """Reads temperature and humidity from the SHT30 sensor."""
    try:

        i2c.writeto(SHT30_ADDRESS, MEASURE_CMD)
        time.sleep(0.05)

        data = i2c.readfrom(SHT30_ADDRESS, 6)
        if len(data) != 6:
            print("Error: Incomplete data received from sensor.")
            return None, None

        temp_raw = int.from_bytes(data[0:2], 'big')
        humidity_raw = int.from_bytes(data[3:5], 'big')

        temp = -45 + (175 * temp_raw / 65535.0)
        humidity = 100 * humidity_raw / 65535.0

        return round(temp, 2), round(humidity, 2)

    except OSError as e:
        print(f"I2C Communication Error: {e}")
        return None, None

if __name__ == "__main__":
    temp, humidity = read_temperature_humidity()
    if temp is not None and humidity is not None:
        print(f"Temperature: {temp} degrees celcius")
        print(f"Humidity: {humidity} %")
    else:
        print("Failed to read valid sensor data.")
