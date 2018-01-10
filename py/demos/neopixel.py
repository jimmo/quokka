import quokka

while True:
  for i in range(10):
    quokka.neopixels.clear()
    quokka.neopixels.set_pixel(i, 64, 0, 0)
    quokka.neopixels.show()
  for i in range(10):
    quokka.neopixels.clear()
    quokka.neopixels.set_pixel(i, 0, 64, 0)
    quokka.neopixels.show()
  for i in range(10):
    quokka.neopixels.clear()
    quokka.neopixels.set_pixel(i, 0, 0, 64)
    quokka.neopixels.show()
