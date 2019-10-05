import sys
import os
import time



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
        amount = 0
        slot_idx = 0
        print('Dispensing %0.2f grams from slot %d' % (amount, slot_idx))

    def calibrate_in_grams(self, weight):
        print('Calibrating %d grams' % weight)