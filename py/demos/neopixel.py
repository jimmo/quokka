import quokka
import time
import neopixel

n = neopixel.NeoPixel()

while True:
  quokka.display.print('red')
  for i in range(8):
    n.clear()
    n[i] = (64, 0, 0)
    n.show()
    time.sleep_ms(200)

  quokka.display.print('green')
  for i in range(8):
    n.clear()
    n[i] = (0, 64, 0)
    n.show()
    time.sleep_ms(200)

  quokka.display.print('blue')
  for i in range(8):
    n.clear()
    n[i] = (0, 0, 64)
    n.show()
    time.sleep_ms(200)
