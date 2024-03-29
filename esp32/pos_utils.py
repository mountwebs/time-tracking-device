# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
# esp.osdebug(None)
# uos.dupterm(None, 1) # disable REPL on UART(0)
import time
import gc
from machine import I2C, Pin, Timer, PWM
import mpu6050
import dist
import os

projects = ["None", "Admin", "oppgave", "møte", "noe", "kaos"]

red_led = PWM(Pin(26), 5000) # esp32: 26, esp8266: 12
green_led = PWM(Pin(18), 5000) # esp32: 26, esp8266: 13
blue_led = PWM(Pin(19), 5000) # esp32: 26, esp8266: 14

red_led.duty(0)
blue_led.duty(0)
green_led.duty(0)

i2c = I2C(scl=Pin(22), sda=Pin(21)) # esp8266: 5,4, esp32: 22,21
accel = mpu6050.accel(i2c)
states = []

session = 0

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

def get_current_coord(data):
    return [int(data['AcZ']), int(data['AcY']), int(data['AcX'])]



def get_closest_side():
    data = get_smoothed_values(n_samples=100)
    position_array = [[14965, 2395, 0],[-410, -14180, 1185],[-2720, 2693, 17093], [-5740, 1970, -15180],[-1970, 18430, 380],[-18270, 2180, 1420]]
    print(dist.get_index_shortest_dist(get_current_coord(data), position_array))

def side_loop():
    while True:
        get_closest_side()
        time.sleep(0.2)

def get_last_state (states):
    if len(states) == 0: return None
    return states[len(states) - 1]["state"]

def get_time_in_state(get_state, states):
    sum = 0
    for i in range(len(states)):
        if states[i]["state"] == get_state and len(states) > i:
            sum += time.ticks_diff(states[i+1]["started"], states[i]["started"])
    return sum

def parse_log_line(log_line):
    log_list = log_line.split(",")
    keys = ["session", "state", "started"]
    return dict(zip(keys,log_list))

def get_last_session():
    dir = os.listdir()
    if not "log.txt" in dir:
        return 0
    else:
        with open("log.txt","r") as f:
            entry = parse_log_line(list(f)[-1])
    return entry["session"].strip('\n')

session = int(get_last_session()) + 1

def time_reporter():
    position_array = [[14965, 2395, 0],[-410, -14180, 1185],[-2720, 2693, 17093], [-5740, 1970, -15180],[-1970, 18430, 380],[-18270, 2180, 1420]]
    cur_orientation = None
    prev_orientation = None
    cur_orientation_started = time.ticks_ms()

    while True:
        acc_data = get_smoothed_values(n_samples=100)
        cur_orientation = dist.get_index_shortest_dist(get_current_coord(acc_data), position_array)
        
        if cur_orientation != prev_orientation:
            cur_orientation_started = time.ticks_ms()
            prev_orientation = cur_orientation

        if time.ticks_diff(time.ticks_ms(), cur_orientation_started) > 1500 and get_last_state(states) != cur_orientation:
            now = time.ticks_ms()
            state = {"state": cur_orientation, "started": now, "session": session}
            states.append(state)
            f = open("log.txt", "a")
            f.write(str(session) + "," + str(state["state"]) + "," + str(now) + "\n")
            f.close()
            print(states)


def convert_from_ms( milliseconds ): 
	seconds, milliseconds = divmod(milliseconds,1000) 
	minutes, seconds = divmod(seconds, 60) 
	hours, minutes = divmod(minutes, 60) 
	seconds = int(seconds + milliseconds/1000)
	return "{}:{}:{}".format(hours, minutes, seconds)


def print_summary():
    state_dict = {}
    with open("log.txt","r") as f:
        lines = f.readlines()

    for i, l in enumerate(lines):
        if len(lines) - 1 > i:
            entry = parse_log_line(l)
            next_entry = parse_log_line(lines[i+1])
            diff = int(next_entry["started"]) - int(entry["started"])
            if entry["state"] in state_dict:
                state_dict[entry["state"]] += diff
            else:
                state_dict[entry["state"]] = diff

    print("\n==Summary==")
    for i, project in enumerate(projects):
        if str(i) in state_dict:
            time_str = convert_from_ms(int(state_dict[str(i)]))

            print(project + ": " + time_str) 
            
