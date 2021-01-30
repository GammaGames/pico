import board
import digitalio
import time

with digitalio.DigitalInOut(board.GP25) as led:
    led.switch_to_output()

    while True:
        led.value = not led.value
        time.sleep(1.0)
