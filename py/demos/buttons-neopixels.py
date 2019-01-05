import quokka
import neopixel

n = neopixel.NeoPixel()

while True:
  n.clear()
  for i, b in enumerate(quokka.buttons):
    n.set_pixel(i, 255 if b.is_pressed() else 0, 0, 0)
  if quokka.button_usr.is_pressed():
    for i in range(4, 8):
      n[i] = (i-4) * 30
  n.show()

  quokka.sleep(50)
