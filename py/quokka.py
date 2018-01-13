import framebuf
import pyb
import machine
import time


class QuokkaNeoPixels():
  def __init__(self):
    self._pin = machine.Pin('X12', machine.Pin.OUT)
    self._pin.off()
    self._buf = bytearray(8*3)
    self.show()

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

  def set_pixel(self, n, r, g, b):
    if n < 0 or n >= 8:
      return
    self._buf[n*3] = g
    self._buf[n*3+1] = r
    self._buf[n*3+2] = b

  def set_pixel_rainbow(self, n, h, l=255):
    r, g, b, = QuokkaNeoPixels._rainbow(h)
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


class QuokkaButton():
  def __init__(self, pin):
    self._pin = pin
    self._last = False
    self._was = False

  def _tick(self):
    if self.is_pressed() and not self._last:
      self._was = True
    self._last = self.is_pressed()

  def was_pressed(self):
    r = self._was
    self._was = False
    return r

  def is_pressed(self):
    return not self._pin.value()


class QuokkaButtons():
  def __init__(self):
    self.a = QuokkaButton(machine.Pin('X18'))
    self.b = QuokkaButton(machine.Pin('X19'))
    self.c = QuokkaButton(machine.Pin('X20'))
    self.d = QuokkaButton(machine.Pin('X21'))
    self.usr = QuokkaButton(machine.Pin('X17'))
    self.all = (self.a, self.b, self.c, self.d,)

  def _tick(self):
    for b in self.all:
      b._tick()


class QuokkaPin():
  def __init__(self, name):
    self._name = name
    self._mode_input()

  def _mode_input(self):
    self._pin = machine.Pin(self._name, machine.Pin.IN, machine.Pin.PULL_NONE)

  def _mode_output(self):
    self._pin = machine.Pin(self._name, machine.Pin.OUT)

  def _mode_pwm(self):
    self._pin = pyb.Pin(self._name)
    if self._name == 'X4':
      self._channel = pyb.Timer(2, freq=1000).channel(4, pyb.Timer.PWM, pin=self._pin)
    elif self._name == 'X3':
      self._channel = pyb.Timer(2, freq=1000).channel(3, pyb.Timer.PWM, pin=self._pin)
    elif self._name == 'X2':
      self._channel = pyb.Timer(2, freq=1000).channel(2, pyb.Timer.PWM, pin=self._pin)
    elif self._name == 'X1':
      self._channel = pyb.Timer(2, freq=1000).channel(1, pyb.Timer.PWM, pin=self._pin)
    elif self._name == 'Y12':
      self._channel = pyb.Timer(1, freq=1000).channel(3, pyb.Timer.PWM, pin=self._pin)
    else:
      raise ValueError('PWM not on pin')

  def on(self):
    self._mode_output()
    self._pin.on()

  def off(self):
    self._mode_output()
    self._pin.off()

  def toggle(self):
    self._mode_output()
    self._pin.toggle()

  def write_digital(self, b):
    self._mode_output()
    self._pin.value(1 if b else 0)

  def read_digital(self):
    self._mode_input()
    return self._pin.value()

  def write_analog(self, percent):
    self._mode_pwm()
    self._channel.pulse_width_percent(percent)


class QuokkaPinAnalogIn(QuokkaPin):
  def __init__(self, name):
    super().__init__(name)

  def _mode_analog(self):
    self._mode_input()
    self._adc = pyb.ADC(self._name)

  def read_analog(self):
    self._mode_analog()
    return self._adc.read()


class QuokkaPinDac(QuokkaPinAnalogIn):
  def __init__(self, name):
    super().__init__(name)

  def _mode_dac(self):
    self._mode_output()

  def write_dac(self, v):
    return


class QuokkaGrove():
  def __init__(self, p0, p1, analog=False):
    if analog:
      if p0 == 'X5':
        self.pin0 = QuokkaPinDac(p0)
      else:
        self.pin0 = QuokkaPinAnalogIn(p0)
      self.pin1 = QuokkaPinAnalogIn(p1)
    else:
      self.pin0 = QuokkaPin(p0)
      self.pin1 = QuokkaPin(p1)


class QuokkaGroves():
  def __init__(self):
    self.a = QuokkaGrove('X9', 'X10') # I2C SCL/SDA
    self.b = QuokkaGrove('Y2', 'Y1')  # UART 6
    self.c = QuokkaGrove('X4', 'X3', analog=True)  # ADC, UART 2
    self.d = QuokkaGrove('X6', 'X8')  # SPI CLK/MOSI
    self.e = QuokkaGrove('X2', 'X1', analog=True)  # ADC, UART 4
    self.f = QuokkaGrove('X5', 'Y12', analog=True) # ADC, DAC pin 0
    self.all = (self.a, self.b, self.c, self.d, self.e, self.f,)


neopixels = QuokkaNeoPixels()
leds = QuokkaLeds()
buttons = QuokkaButtons()
groves = QuokkaGroves()

sleep = time.sleep_ms
sleep_us = time.sleep_us


_internal_spi = machine.SPI('Y', baudrate=2000000)
spi = machine.SPI('X')
i2c = machine.I2C('X')

import drivers

class QuokkaDisplay(drivers.SSD1306_SPI):
  def __init__(self, spi):
    super().__init__(128, 64, spi, machine.Pin('X11', machine.Pin.OUT), machine.Pin('X22', machine.Pin.OUT), machine.Pin('Y5', machine.Pin.OUT), external_vcc=True)
    self.text_x = 0
    self.text_y = 0

  def print(self, text, color=1):
    pass

  def text(self, text, x, y, color, scale=1):
    if scale == 1:
      super().text(text, x, y, color)
    else:
      # This could be smaller - only needs to be big enough to hold text.
      buf = bytearray(self.pages * self.width)
      fb = framebuf.FrameBuffer(buf, self.width, self.height, framebuf.MONO_VLSB)
      bg = 1 - color
      fb.fill(bg)
      fb.text(text, 0, 0, color)
      self.scale_blit(fb, x, y, scale, bg)

  def scale_blit(self, fb, x, y, scale, key=None):
    if scale == 1:
      self.blit(fb, x, y, key)
    else:
      for xx in range(self.width // scale):
        for yy in range(self.height // scale):
          c = fb.pixel(xx, yy)
          if key is None or c != key:
            self.fill_rect(x + xx * scale, y + yy * scale, scale, scale, c)


display = QuokkaDisplay(_internal_spi)

_imu = drivers.MPU9250('Y')

accelerometer = _imu.accel
compass = _imu.mag
gyro = _imu.gyro


radio = drivers.QuokkaRadio(machine.Pin('Y4', machine.Pin.OUT), _internal_spi)

def temperature():
  return _imu.temperature

def running_time():
  return pyb.millis()

def _on_tick(t):
  buttons._tick()

timer_tick = pyb.Timer(1, freq=200, callback=_on_tick)

__all__ = ['display', 'neopixels', 'radio', 'buttons', 'leds', 'sleep', 'sleep_us', 'temperature', 'running_time', 'accelerometer', 'gyro', 'compass',]
