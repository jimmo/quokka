import quokka
import time

while True:
  quokka.display.fill(0)
  quokka.display.text('red', 5, 5, 1)
  quokka.display.show()
  for i in range(8):
    quokka.neopixels.clear()
    quokka.neopixels.set_pixel(i, 64, 0, 0)
    quokka.neopixels.show()
    time.sleep_ms(200)

  quokka.display.fill(0)
  quokka.display.text('green', 5, 5, 1)
  quokka.display.show()
  for i in range(8):
    quokka.neopixels.clear()
    quokka.neopixels.set_pixel(i, 0, 64, 0)
    quokka.neopixels.show()
    time.sleep_ms(200)

  quokka.display.fill(0)
  quokka.display.text('blue', 5, 5, 1)
  quokka.display.show()
  for i in range(8):
    quokka.neopixels.clear()
    quokka.neopixels.set_pixel(i, 0, 0, 64)
    quokka.neopixels.show()
    time.sleep_ms(200)
