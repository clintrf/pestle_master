import sys
import os
import time

import RPi.GPIO as GPIO
import l293d.driver as l293d
from hx711 import HX711


# Pins are in GPIO.BCM mode
L293D_ENB_PIN = 22
L293D_INPUT1_PIN = 27
L293D_INPUT2_PIN = 17


class DispenserInterface(object):
    def clean_and_exit(self):
        raise NotImplementedError()

    def dispense(self, slot_idx, amount):
        raise NotImplementedError()

    def calibrate_in_grams(self, weight):
        raise NotImplementedError()


class TestDispenser(DispenserInterface):
    def __init__(self):
        print('Creating TestDispenser')

    def clean_and_exit(self):
        print('Dispenser Exiting')

    def dispense(self, slot_idx, amount):
        print('Dispensing %0.2f grams from slot %d' % (amount, slot_idx))

    def calibrate_in_grams(self, weight):
        print('Calibrating %d grams' % weight)


class Dispenser(DispenserInterface):
    def __init__(self):
        # Set the pins for the scale. Pins are in GPIO.BCM mode
        self._hx = HX711(5, 6)
        # Set and initialize the pins for the 2 motors
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(L293D_INPUT1_PIN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(L293D_INPUT2_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(L293D_ENB_PIN, GPIO.OUT)

        # Set the read in format for first the Pi and then the Hx711 board (MSB/LSB most/least sig bit)
        self._hx.set_reading_format("MSB", "MSB")

        # HOW TO CALCULATE THE REFFERENCE UNIT
        # If 2000 grams is 184000 then 1 gram is 184000 / 2000 = 92.
        # hx.set_reference_unit(92)
        # hx.set_reference_unit(calibrateInGrams(self.weight))
        self._hx.set_reference_unit(14550)

        # Reset and tare scale
        self._hx.reset()
        self._hx.tare()
        print('Tare done!')

    def clean_and_exit(self):
        print('Cleaning...')
        GPIO.cleanup()
        print('Bye!')
        sys.exit()

    def dispense(self, slot_idx, amount):
        print('Dispensing %0.2f grams from slot %d' % (amount, slot_idx))

        if slot_idx == 0:  # if it's salt
            motor_pin = L293D_ENB_PIN
        elif slot_idx == 1:  # if it's pepper
            motor_pin = L293D_ENB_PIN
        else:
            return 0

        motor = GPIO.PWM(motor_pin,50) # pwm frequency: 50hz
        val = self._hx.get_weight(5)
        while val <= amount:
            print(val)
            motor.start(50)  # duty cycle: check to see if we need to increase the param
        motor.stop()
        #print("Finished dispensing %0.2f grams of from slot %d"% (amount, slot_idx))

    def calibrate_in_grams(self, weight=100):
        self._hx.set_reference_unit(1)
        val = self._hx.get_weight(20)
        print(val)
        # hx.power_down()
        # hx.power_up()
        # time.sleep(0.1)
        ref_unit = val / weight
        self._hx.set_reference_unit(ref_unit)
