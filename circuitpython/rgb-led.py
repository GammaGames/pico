import board
import digitalio
import analogio
import time
import pwmio

MAX = 65534
MIN = 0

left_switch = digitalio.DigitalInOut(board.GP7)
left_switch.switch_to_input(pull=digitalio.Pull.UP)
right_switch = digitalio.DigitalInOut(board.GP6)
right_switch.switch_to_input(pull=digitalio.Pull.UP)
dial = analogio.AnalogIn(board.GP26_A0)

red = pwmio.PWMOut(board.GP10, duty_cycle = MAX)
green = pwmio.PWMOut(board.GP12, duty_cycle = MAX)
blue = pwmio.PWMOut(board.GP14, duty_cycle = MAX)

while True:
    target = None
    if left_switch.value and right_switch.value:
        target = blue
    elif left_switch.value:
        target = red
    elif right_switch.value:
        target = green

    if target is not None:
        dial_value = round((dial.value - MIN) / (MAX - MIN), 2)
        if dial_value < 0.02:
            dial_value = 0
        target.duty_cycle = round((1.0 - dial_value) * (MAX))
    time.sleep(0.1)
