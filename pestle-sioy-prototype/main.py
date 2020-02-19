from time import sleep

from RPi import GPIO

DIRX_PIN = 26
STEPX_PIN = 12


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIRX_PIN, GPIO.OUT)
    GPIO.setup(STEPX_PIN, GPIO.OUT)

    cw = True
    while True:
        if cw:
            GPIO.output(DIRX_PIN, GPIO.HIGH)
        else:
            GPIO.output(DIRX_PIN, GPIO.LOW)
        cw = not cw
        print("switch")
        for _ in range(1000):
            GPIO.output(STEPX_PIN, GPIO.HIGH)
            sleep(.00208)
            GPIO.output(STEPX_PIN, GPIO.LOW)
            sleep(.00208)


if __name__ == '__main__':
    main()

