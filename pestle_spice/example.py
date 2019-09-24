from dispenser import TestDispenser, Dispenser
import time
import sys

import RPi.GPIO as GPIO
from hx711 import HX711

motorPin = 00
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPin, GPIO.OUT)

motor = GPIO.PWM(servoPin,50) # pwm 50hz
motor.start(2)
motor.stop()


def cleanAndExit():
    print ("Cleaning...")

    GPIO.cleanup()
        
    print ("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(14550)

hx.reset()

hx.tare()

print ("Tare done! Add weight now...")

while True:
    try:

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()