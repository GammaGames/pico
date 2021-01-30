from adafruit_hid.gamepad import Gamepad
import board
import digitalio
import analogio
import time
import pwmio
import usb_hid


class Button():
    def __init__(self, pin, button):
        self.pin = pin
        self.button = digitalio.DigitalInOut(self.pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        self.index = button
        self.last_value = None

    def changed(self):
        is_changed = self.last_value != self.button.value
        self.last_value = self.button.value
        return is_changed

    def get_value(self):
        return self.button.value


gamepad = Gamepad(usb_hid.devices)
button_pins = (board.GP13, board.GP14)
gamepad_buttons = (1, 2)
buttons = [Button(pin, gamepad_buttons[index]) for index, pin in enumerate(button_pins)]

while True:
    for i, button in enumerate(buttons):
        if button.changed():
            if button.get_value():
                gamepad.release_buttons(button.index)
                print(" release", button.index, end="")
            else:
                gamepad.press_buttons(button.index)
                print(" press", button.index, end="")
    time.sleep(0.1)
