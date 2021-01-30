import board
import digitalio
import analogio
import time
import pwmio

MAX = 65535
MIN = 0

dial = analogio.AnalogIn(board.GP26_A0)
led = pwmio.PWMOut(
    board.GP9,
    duty_cycle = 0,
    frequency=5000
)

while True:
    dial_value = round((dial.value - MIN) / (MAX - MIN), 2)
    if dial_value < 0.02:
        dial_value = 0
    led.duty_cycle = round(dial_value * 65535)
    time.sleep(0.1)
