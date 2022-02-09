import board
import time
import audiomp3
import audiopwmio
import neopixel
from rainbowio import colorwheel
# https://learn.adafruit.com/adafruit-feather-rp2040-pico/built-in-neopixel-led
# https://learn.adafruit.com/mp3-playback-rp2040

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
audio = audiopwmio.PWMAudioOut(board.TX)
decoder = audiomp3.MP3Decoder(open("slow.mp3", "rb"))

pixel.fill((255, 0, 0))
pixel.brightness = 0.1
time.sleep(0.5)
pixel.brightness = 0
time.sleep(0.5)
pixel.fill((255, 255, 0))
pixel.brightness = 0.1
time.sleep(0.5)
pixel.brightness = 0
time.sleep(0.5)
pixel.fill((0, 255, 0))
pixel.brightness = 0.1
time.sleep(0.5)
pixel.brightness = 0
time.sleep(0.5)

audio.play(decoder)
while audio.playing:
    pixel.brightness = 0.1
    pixel[0] = colorwheel(int(time.monotonic_ns() * 0.0000001) % 255)
