import board
import digitalio
import time

button = digitalio.DigitalInOut(board.GP13)
button.switch_to_input(pull=digitalio.Pull.UP)

led = digitalio.DigitalInOut(board.GP14)
led.switch_to_output()

while True:
    led.value = not button.value
    time.sleep(0.1)
