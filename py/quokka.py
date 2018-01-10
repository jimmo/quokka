import pyb
import machine

import drivers

__all__ = ['display', 'neopixels', 'radio']


class QuokkaDisplay(drivers.SSD1306_SPI):
  def __init__(self, spi):
    super().__init__(128, 64, spi, machine.Pin('X11', machine.Pin.OUT), machine.Pin('X22', machine.Pin.OUT), machine.Pin('Y5', machine.Pin.OUT), external_vcc=True)


class QuokkaRadio():
  def __init__(self, spi):
    pass


def _rainbow(h):
  # h is hue between 0-119.
  if h < 20:
    return (255, (h * 255) // 20, 0,)
  elif h < 40:
    return (((40-h) * 255) // 20, 255, 0,)
  elif h < 60:
    return (0, 255, ((h-40) * 255) // 20,)
  elif h < 80:
    return (0, ((80-h) * 255) // 20, 255,)
  elif h < 100:
    return (((h-80) * 255) // 20, 0, 255,)
  else:
    return (255, 0, ((120-h) * 255) // 20,)


class QuokkaNeoPixels():
  def __init__(self):
    self._pin = machine.Pin('X12', machine.Pin.OUT)
    self._buf = bytearray(8*3)

  def set_pixel(self, n, r, g, b):
    if n < 0 or n >= 8:
      return
    self._buf[n*3] = g
    self._buf[n*3+1] = r
    self._buf[n*3+2] = b

  def set_pixel_rainbow(self, n, h, l=255):
    r, g, b, = rainbow(h)
    self.set_pixel(n, r * 255 // 255, g * 255 // 255, b * 255 // 255,)

  def show(self):
    self._pin.neo(self._buf)

  def clear(self):
    self.all(0, 0, 0)

  def all(self, r, g, b):
    for i in range(10):
      self.set_pixel(i, r, g, b,)


class QuokkaLeds():
  def __init__(self):
    self.red = pyb.LED(1)
    self.green = pyb.LED(2)
    self.orange = pyb.LED(3)
    self.blue = pyb.LED(4)
    self.all = (self.red, self.orange, self.green, self.blue,)

  def clear(self):
    for l in self.all:
      l.off()

_internal_spi = machine.SPI('Y', baudrate=10000000)

display = QuokkaDisplay(_internal_spi)
radio = QuokkaRadio(_internal_spi)
neopixels = QuokkaNeoPixels()
leds = QuokkaLeds()
