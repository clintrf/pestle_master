import sys
import time
import RPi.GPIO as GPIO
#from hx711 import HX711

#Pins are in GPIO.BCM mode
DIRX_PIN = 6            #Direction GPIO Pin for Motor X
DIRY_PIN = 26           #Direction GPIO Pin for Motor Y

STEPX_PIN = 5           #Step GPIO Pin for Motor X
STEPY_PIN = 13          #Step GPIO Pin for Motor Y
SLEEP_PIN = 17          #dual sleep

CW = 1                  #Clockwise Rotation
CCW = 0                 #Counterclockwise Rotation
SPR = 325               #Steps per Revolution (360/?)

SWITCHX_PIN = 27        #Switch Pin for X track
SWITCHY_PIN = 22        #Switch Pin for Y track


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

    def move(self, slot_idx, slot_idy):
        print('moving to %d,%d x,y' % (slot_idx , slot_idy))
        for i in range(5):
            time.sleep(1)

    def dispense(self, amount):
        print('Dispensing %0.2f grams' % (amount))
        for i in range(0,amount,2):
            print(i)
            time.sleep(1)

    def calibrate_scale(self, weight):
        print('Calibrating %d grams' % weight)

    def calibrate_track(self):
        print('Reseting Track')


class Dispenser(DispenserInterface):
    def __init__(self):
        print('Creating TestDispenser')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIRX_PIN, GPIO.OUT)
        GPIO.setup(DIRY_PIN, GPIO.OUT)
        
        GPIO.setup(STEPX_PIN, GPIO.OUT)
        GPIO.setup(STEPY_PIN, GPIO.OUT)

        GPIO.setup(SLEEP_PIN, GPIO.OUT)

        GPIO.setup(SWITCHX_PIN, GPIO.IN)
        GPIO.setup(SWITCHY_PIN, GPIO.IN)

        GPIO.output(SLEEP_PIN, GPIO.LOW)

        #from hx711 import HX711 #import library for scale

    def clean_and_exit(self):
        print('Dispenser Exiting')
        GPIO.cleanup()
        print('Bye!')
        sys.exit()

    def move(self, slot_idx, slot_idy):
        print('moving to %d,%d x,y' % (slot_idx , slot_idy))
        
        GPIO.output(DIRX_PIN, CW)       #Set init direction of motor X
        GPIO.output(DIRY_PIN, CW)       #Set init direction of motor Y

        GPIO.output(SLEEP_PIN, GPIO.HIGH)
        time.sleep(.25)

        for x in range(SPR*slot_idx):
            GPIO.output(STEPX_PIN, GPIO.HIGH)
            time.sleep(.00208)
            GPIO.output(STEPX_PIN, GPIO.LOW)
            time.sleep(.00208)
        time.sleep(.5)
        
        for y in range(SPR*slot_idy):
            GPIO.output(STEPY_PIN, GPIO.HIGH)
            time.sleep(.00208)
            GPIO.output(STEPY_PIN, GPIO.LOW)
            time.sleep(.00208)

        GPIO.output(SLEEP_PIN, GPIO.LOW)

    def dispense(self, amount):
        print('Dispensing %0.2f grams' % (amount))
        for i in range(0,amount,2):
            print(i)
            time.sleep(1)

    def calibrate_scale(self, weight):
        print('Calibrating %d grams' % weight)
        for i in range(0,3):
            time.sleep(1)


    def calibrate_track(self):
        print('Reseting Track')
        
        GPIO.output(DIRX_PIN, CCW)       #Set init direction of motor X
        GPIO.output(DIRY_PIN, CCW)       #Set init direction of motor Y
        
        GPIO.output(SLEEP_PIN, GPIO.HIGH)

        while GPIO.input(SWITCHX_PIN) == 0 :
            GPIO.output(STEPX_PIN, GPIO.HIGH)
            time.sleep(.00208)
            GPIO.output(STEPX_PIN, GPIO.LOW)
            time.sleep(.00208)
        print('switch X pressed')    
        time.sleep(.5)
        
        while GPIO.input(SWITCHY_PIN) == 0:
            GPIO.output(STEPY_PIN, GPIO.HIGH)
            time.sleep(.00208)
            GPIO.output(STEPY_PIN, GPIO.LOW)
            time.sleep(.00208)
        
        GPIO.output(SLEEP_PIN, GPIO.LOW)



        print('switch Y pressed')
        print('Finished Reseting')
        print('')


