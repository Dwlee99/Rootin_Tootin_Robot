import os
import RPi.GPIO as GPIO
import time
from gun_camera import take_photo, color_in_center
from bluedot.btcomm import BluetoothClient, BluetoothAdapter
from datetime import datetime
from time import sleep
from signal import pause

a = BluetoothAdapter()
print(a.paired_devices)

def data_received(data):
    print("recv - {}".format(data))

print("Connecting")
connected = False
while not connected:
    try:
        c = BluetoothClient(a.paired_devices[0][1], data_received)
        connected = True
    except:
        sleep(10)

print("Sending")

code_run = True

button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prev_state = False

def button_callback(channel):
    print("button pressed")
    image = take_photo()
    color = color_in_center(image)
    print(color)
    c.send(color)

GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback, bouncetime=1000)

try:
    while code_run:
        sleep(1)
finally:
    c.disconnect()
    GPIO.cleanup()
