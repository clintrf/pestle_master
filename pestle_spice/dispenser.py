import sys


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
        import RPi.GPIO as GPIO
        from hx711 import HX711
        # Set the pins for the scale. Pins are in GPIO.BCM mode
        self._hx = HX711(5, 6)

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
        val = self._hx.get_weight(2)
        print(val)

    def calibrate_in_grams(self, weight=100):
        self._hx.set_reference_unit(1)
        val = self._hx.get_weight(20)
        print(val)
        # hx.power_down()
        # hx.power_up()
        # time.sleep(0.1)
        ref_unit = val / weight
        self._hx.set_reference_unit(ref_unit)
