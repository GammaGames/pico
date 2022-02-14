import board
import time
import audiomp3
import audiopwmio
import neopixel
from rainbowio import colorwheel
import board
import displayio
import digitalio
import terminalio
import os
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from adafruit_debouncer import Debouncer
import storage

switch = digitalio.DigitalInOut(board.D10)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the D10 is connected to ground with a wire
# CircuitPython can write to the drive
try:
    storage.remount("/", switch.value)
except:
    print("Mounted via USB, not remounting storage")

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Make the display context
splash = displayio.Group()
display.show(splash)
color_bitmap = displayio.Bitmap(128, 32, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000  # White
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)
text_area = label.Label(terminalio.FONT, color=0xFFFF00, x=0, y=4)
splash.append(text_area)

def display_text(value):
    text_area.text = value
    display.refresh()

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0

def play(filename):
    with audiopwmio.PWMAudioOut(board.TX) as audio:
        with audiomp3.MP3Decoder(open(f"/media/{filename}", "rb")) as decoder:
            audio.play(decoder)
            while audio.playing:
                pixel.brightness = 0.1
                pixel[0] = colorwheel(int(time.monotonic() * 50))
    pixel.brightness = 0

button_a = digitalio.DigitalInOut(board.D9)
button_a.switch_to_input(pull=digitalio.Pull.UP)
a = Debouncer(button_a)
button_b = digitalio.DigitalInOut(board.D6)
button_b.switch_to_input(pull=digitalio.Pull.UP)
b = Debouncer(button_b)
button_c = digitalio.DigitalInOut(board.D5)
button_c.switch_to_input(pull=digitalio.Pull.UP)
c = Debouncer(button_c)

def write_config(timer, index):
    try:
        with open("/.conf", "w") as out_file:
            out_file.write(f"{timer}\n{index}")
    except Exception:
        pass
    
def read_config():
    if ".conf" in os.listdir("/"):
        with open("/.conf", "r") as in_file:
            config = in_file.read().split("\n")
            timer = int(config[0])
            index = int(config[1])
    else:
        timer = 3
        index = 0
    return (timer, index)
    
mode = 0
timer, index = read_config()
start = time.monotonic()
should_update_start = time.monotonic()
files = os.listdir("/media")
files.sort()
previous_index = None
refresh = True

while True:
    now = time.monotonic()
    a.update()
    b.update()
    c.update()

    if not a.value and a.fell:
        if mode == 0:
            timer += 1
        elif mode == 1:
            index += 1
        write_config(timer, index)
        refresh = True
    elif not b.value and b.fell:
        mode = (mode + 1) % 2
    elif not c.value and c.fell:
        if mode == 0:
            timer -= 1
        elif mode == 1:
            index -= 1
        write_config(timer, index)
        refresh = True

    if not refresh and now - should_update_start > 1.0:
        refresh = True
        should_update_start = now

    if refresh:
        percent = ((now - start) / (timer * 60)) * 100
        text = f"{timer}min"
        if mode == 0:
            text += "<: "
        else:
            text += ": >"
        text += f"{files[index % len(files)]}\n{percent:.0f}%"
        display_text(text)
        refresh = False
    previous_index = index

    if now - start > timer * 60:
        display_text("TEA DONE!")
        play(files[index % len(files)])
    else:
        time.sleep(0.1)
