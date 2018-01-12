from quokka import *
import time

def pulse(g):
  while True:
    neopixels.set_pixel(0, 255, 0, 0)
    neopixels.show()
    g.pin0.on()
    time.sleep_ms(1000)
    neopixels.set_pixel(0, 0, 0, 0)
    neopixels.show()
    g.pin0.off()
    time.sleep_ms(1000)

    neopixels.set_pixel(1, 255, 0, 0)
    neopixels.show()
    g.pin1.on()
    time.sleep_ms(1000)
    neopixels.set_pixel(1, 0, 0, 0)
    neopixels.show()
    g.pin1.off()
    time.sleep_ms(1000)
