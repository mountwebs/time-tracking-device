# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
# esp.osdebug(None)
# uos.dupterm(None, 1) # disable REPL on UART(0)
import time
import gc
from machine import I2C, Pin, Timer, PWM
import mpu6050

red_led = PWM(Pin(12), 5000)
blue_led = PWM(Pin(14), 5000)
green_led = PWM(Pin(13), 5000)

red_led.duty(0)
blue_led.duty(0)
green_led.duty(0)

i2c = I2C(scl=Pin(5), sda=Pin(4))
accel = mpu6050.accel(i2c)
#import webrepl
# webrepl.start()

start = time.ticks_ms()


def setRGB(r, g, b):
    red_led.duty(r)
    blue_led.duty(g)
    green_led.duty(b)


def get_smoothed_values(n_samples=10, calibration=None):
    """
    Get smoothed values from the sensor by sampling
    the sensor `n_samples` times and returning the mean.

    If passed a `calibration` dictionary, subtract these
    values from the final sensor value before returning.
    """
    result = {}
    for _ in range(n_samples):
        data = accel.get_values()

        for key in data.keys():
            # Add on value / n_samples to produce an average
            # over n_samples, with default of 0 for first loop.
            result[key] = result.get(key, 0) + (data[key] / n_samples)

    if calibration:
        # Remove calibration adjustment.
        for key in calibration.keys():
            result[key] -= calibration[key]

    return result

def find_pos():
    while True:
        data = get_smoothed_values(n_samples=1000)
        print(data)


def testing():
    current_orientation = None
    prev_orientation = None

    while True:
        data = get_smoothed_values(n_samples=100)
        # print(
        #     '\t'.join('{0}:{1:>10.1f}'.format(k, data[k])
        #               for k in sorted(data.keys())),
        #     end='\r')

        prev_orientation = current_orientation

        if data["AcX"] > 10000:
            current_orientation = "right"

        if data["AcX"] < 10000 and data["AcX"] > -10000:
            current_orientation = "flat"

        if data["AcX"] < -10000:
            current_orientation = "left"

        print(current_orientation)

        def sendRight():
            print("r")
            setRGB(255, 0, 0)

        def sendLeft():
            print("l")
            setRGB(0, 255, 0)

        def sendFlat():
            print("f")
            setRGB(0, 0, 255)

        action = {
            'right': sendRight,
            'flat': sendFlat,
            'left': sendLeft,
        }

        if current_orientation != prev_orientation:
            print("changed orientation!")
            # compute time difference
            delta = time.ticks_diff(time.ticks_ms(), start)
            # if delta > 5000:
            action[current_orientation]()

            start = time.ticks_ms()  # get millisecond counter

        print(data)