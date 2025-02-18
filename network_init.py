import network
import socket
from time import sleep
import machine
from picozero import pico_led, pico_temp_sensor
import rp2
import sys

# add wifi credentials 
ssid = "_"
password = "_"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        if rp2.bootsel_button() == 1:
            sys.exit()
        print('Waiting for connection...')
        pico_led.on()
        sleep(0.5)
        pico_led.off()
        sleep(0.5)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    pico_led.on()
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state, water):
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <form action="./close">
        <input type="submit" value="Stop server" />
            <p>LED is {state}</p>
            <p>Temperature is about {temperature} degrees Celcius </p>
            <p>Water sensor data: {water} </p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    state = 'ON'
    pico_led.on()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        elif request == '/close?':
            sys.exit()
        temperature = pico_temp_sensor.temp
        water = machine.ADC(26).read_u16()
        html = webpage(temperature, state, water)
        client.send(html)
        client.close()

ip = connect()
connection = open_socket(ip)
serve(connection)

