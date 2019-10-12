import RPi.GPIO as GPIO
import time
import threading


class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        self._pd_sck = pd_sck

        self._dout = dout

        # Mutex for reading from the HX711, in case multiple threads in client
        # software try to access get values from the class at the same time.
        self._read_lock = threading.Lock()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pd_sck, GPIO.OUT)
        GPIO.setup(self._dout, GPIO.IN)

        self._gain = 0

        # The value returned by the hx711 that corresponds to your reference
        # unit AFTER dividing by the SCALE.
        self._reference_unit = 1
        self._reference_unit_b = 1

        self._offset = 1
        self._offset_b = 1
        self._last_val = 0

        self._debug_printing = False

        self._byte_format = 'MSB'
        self._bit_format = 'MSB'

        self.set_gain(gain)

        # TODO: Think about whether this is necessary.
        time.sleep(1)

    @staticmethod
    def convert_twos_compliment_to_24_bit(input_value):
        return -(input_value & 0x800000) + (input_value & 0x7fffff)

    def is_ready(self):
        return GPIO.input(self._dout) == 0

    def set_gain(self, gain):
        if gain is 128:
            self._gain = 1
        elif gain is 64:
            self._gain = 3
        elif gain is 32:
            self._gain = 2

        GPIO.output(self._pd_sck, False)

        # Read out a set of raw bytes and throw it away.
        self.read_raw_bytes()

    def get_gain(self):
        if self._gain == 1:
            return 128
        if self._gain == 3:
            return 64
        if self._gain == 2:
            return 32

        # Shouldn't get here.
        return 0

    def read_next_bit(self):
        # Clock HX711 Digital Serial Clock (PD_SCK).  DOUT will be
        # ready 1us after PD_SCK rising edge, so we sample after
        # lowering PD_SCL, when we know DOUT will be stable.
        GPIO.output(self._pd_sck, True)
        GPIO.output(self._pd_sck, False)
        value = GPIO.input(self._dout)

        # Convert Boolean to int and return it.
        return int(value)

    def read_next_byte(self):
        byte_value = 0

        # Read bits and build the byte from top, or bottom, depending
        # on whether we are in MSB or LSB bit mode.
        for x in range(8):
            if self._bit_format == 'MSB':
                byte_value <<= 1
                byte_value |= self.read_next_bit()
            else:
                byte_value >>= 1
                byte_value |= self.read_next_bit() * 0x80

        # Return the packed byte.
        return byte_value

    def read_raw_bytes(self):
        # Wait for and get the Read Lock, incase another thread is already
        # driving the HX711 serial interface.
        self._read_lock.acquire()

        # Wait until HX711 is ready for us to read a sample.
        while not self.is_ready():
            pass

        # Read three bytes of data from the HX711.
        first_byte = self.read_next_byte()
        second_byte = self.read_next_byte()
        third_byte = self.read_next_byte()

        # HX711 Channel and gain factor are set by number of bits read
        # after 24 data bits.
        for i in range(self._gain):
            # Clock a bit out of the HX711 and throw it away.
            self.read_next_bit()

        # Release the Read Lock, now that we've finished driving the HX711
        # serial interface.
        self._read_lock.release()

        # Depending on how we're configured, return an orderd list of raw byte
        # values.
        if self._byte_format == 'LSB':
            return [third_byte, second_byte, first_byte]
        else:
            return [first_byte, second_byte, third_byte]

    def read_long(self):
        # Get a sample from the HX711 in the form of raw bytes.
        data_bytes = self.read_raw_bytes()

        if self._debug_printing:
            print(data_bytes)

        # Join the raw bytes into a single 24bit 2s complement value.
        twos_complement_value = ((data_bytes[0] << 16) |
                               (data_bytes[1] << 8) |
                               data_bytes[2])

        if self._debug_printing:
            print('Twos: 0x%06x' % twos_complement_value)

        # Convert from 24bit twos-complement to a signed value.
        signed_int_value = self.convert_twos_compliment_to_24_bit(twos_complement_value)

        # Record the latest sample value we've read.
        self._last_val = signed_int_value

        # Return the sample value we've read from the HX711.
        return signed_int_value

    def read_average(self, times=3):
        # Make sure we've been asked to take a rational amount of samples.
        if times <= 0:
            raise ValueError("HX711()::read_average(): times must >= 1!!")

        # If we're only average across one value, just read it and return it.
        if times == 1:
            return self.read_long()

        # If we're averaging across a low amount of values, just take the
        # median.
        if times < 5:
            return self.read_median(times)

        # If we're taking a lot of samples, we'll collect them in a list, remove
        # the outliers, then take the mean of the remaining set.
        value_list = []

        for x in range(times):
            value_list += [self.read_long()]

        value_list.sort()

        # We'll be trimming 20% of outlier samples from top and bottom of collected set.
        trim_amount = int(len(value_list) * 0.2)

        # Trim the edge case values.
        value_list = value_list[trim_amount:-trim_amount]

        # Return the mean of remaining samples.
        return sum(value_list) / len(value_list)

    # A median-based read method, might help when getting random value spikes
    # for unknown or CPU-related reasons
    def read_median(self, times=3):
        if times <= 0:
            raise ValueError("HX711::read_median(): times must be greater than zero!")

        # If times == 1, just return a single reading.
        if times == 1:
            return self.read_long()

        value_list = []

        for x in range(times):
            value_list += [self.read_long()]

        value_list.sort()

        # If times is odd we can just take the centre value.
        if (times & 0x1) == 0x1:
            return value_list[int(len(value_list) / 2)]
        else:
            # If times is even we have to take the arithmetic mean of
            # the two middle values.
            midpoint = len(value_list) / 2
            return sum(value_list[midpoint:midpoint + 2]) / 2.0

    # Compatibility function, uses channel A version
    def get_value(self, times=3):
        return self.get_value_a(times)

    def get_value_a(self, times=3):
        return self.read_median(times) - self._offset

    def get_value_b(self, times=3):
        # for channel B, we need to set_gain(32)
        g = self.get_gain()
        self.set_gain(32)
        value = self.read_median(times) - self._offset_b
        self.set_gain(g)
        return value

    # Compatibility function, uses channel A version
    def get_weight(self, times=3):
        return self.get_weight_a(times)

    def get_weight_a(self, times=3):
        value = self.get_value_a(times)
        value = value / self._reference_unit
        return value

    def get_weight_b(self, times=3):
        value = self.get_value_b(times)
        value = value / self._reference_unit_b
        return value

    # Sets tare for channel A for compatibility purposes
    def tare(self, times=15):
        self.tare_a(times)

    def tare_a(self, times=15):
        # Backup REFERENCE_UNIT value
        backup_reference_unit = self.get_reference_unit_a()
        self.set_reference_unit_a(1)

        value = self.read_average(times)

        if self._debug_printing:
            print('Tare A value:', value)

        self.set_offset_a(value)

        # Restore the reference unit, now that we've got our offset.
        self.set_reference_unit_a(backup_reference_unit)

        return value

    def tare_b(self, times=15):
        # Backup REFERENCE_UNIT value
        backup_reference_unit = self.get_reference_unit_b()
        self.set_reference_unit_b(1)

        # for channel B, we need to set_gain(32)
        backup_gain = self.get_gain()
        self.set_gain(32)

        value = self.read_average(times)

        if self._debug_printing:
            print('Tare B value:', value)

        self.set_offset_b(value)

        # Restore gain/channel/reference unit settings.
        self.set_gain(backup_gain)
        self.set_reference_unit_B(backup_reference_unit)

        return value

    def set_reading_format(self, byte_format="LSB", bit_format="MSB"):
        if byte_format == "LSB":
            self._byte_format = byte_format
        elif byte_format == "MSB":
            self._byte_format = byte_format
        else:
            raise ValueError("Unrecognised byte_format: \"%s\"" % byte_format)

        if bit_format == "LSB":
            self._bit_format = bit_format
        elif bit_format == "MSB":
            self._bit_format = bit_format
        else:
            raise ValueError("Unrecognised bitformat: \"%s\"" % bit_format)

    # sets offset for channel A for compatibility reasons
    def set_offset(self, offset):
        self.set_offset_a(offset)

    def set_offset_a(self, offset):
        self._offset = offset

    def set_offset_b(self, offset):
        self._offset_b = offset

    def get_offset(self):
        return self.get_offset_a()

    def get_offset_a(self):
        return self._offset

    def get_offset_b(self):
        return self._offset_b

    def set_reference_unit(self, reference_unit):
        self.set_reference_unit_a(reference_unit)

    def set_reference_unit_a(self, reference_unit):
        # Make sure we aren't asked to use an invalid reference unit.
        if reference_unit == 0:
            raise ValueError("HX711::set_reference_unit_A() can't accept 0 as a reference unit!")

        self._reference_unit = reference_unit

    def set_reference_unit_b(self, reference_unit):
        # Make sure we aren't asked to use an invalid reference unit.
        if reference_unit == 0:
            raise ValueError("HX711::set_reference_unit_A() can't accept 0 as a reference unit!")

        self._reference_unit_b = reference_unit

    def get_reference_unit(self):
        return self.get_reference_unit_a()

    def get_reference_unit_a(self):
        return self._reference_unit

    def get_reference_unit_b(self):
        return self._reference_unit_b

    def power_down(self):
        # Wait for and get the Read Lock, incase another thread is already
        # driving the HX711 serial interface.
        self._read_lock.acquire()

        # Cause a rising edge on HX711 Digital Serial Clock (PD_SCK).  We then
        # leave it held up and wait 100 us.  After 60us the HX711 should be
        # powered down.
        GPIO.output(self._pd_sck, False)
        GPIO.output(self._pd_sck, True)

        time.sleep(0.0001)

        # Release the Read Lock, now that we've finished driving the HX711
        # serial interface.
        self._read_lock.release()

    def power_up(self):
        # Wait for and get the Read Lock, incase another thread is already
        # driving the HX711 serial interface.
        self._read_lock.acquire()

        # Lower the HX711 Digital Serial Clock (PD_SCK) line.
        GPIO.output(self._pd_sck, False)

        # Wait 100 us for the HX711 to power back up.
        time.sleep(0.0001)

        # Release the Read Lock, now that we've finished driving the HX711
        # serial interface.
        self._read_lock.release()

        # HX711 will now be defaulted to Channel A with gain of 128.  If this
        # isn't what client software has requested from us, take a sample and
        # throw it away, so that next sample from the HX711 will be from the
        # correct channel/gain.
        if self.get_gain() != 128:
            self.read_raw_bytes()

    def reset(self):
        self.power_down()
        self.power_up()
