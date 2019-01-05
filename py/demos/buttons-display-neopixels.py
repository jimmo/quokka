import quokka
import neopixel
import radio

n = neopixel.NeoPixel()

quokka.display.print(radio.version())
quokka.sleep(1000)
n.clear()
n.show()


while True:
  quokka.display.fill(0)

  if quokka.button_a.is_pressed():
    quokka.display.print('a')
    n.set_pixel(0, 255, 0, 0)
  else:
    n.set_pixel(0, 0, 0, 0)

  if quokka.button_b.is_pressed():
    quokka.display.print('b')
    n.set_pixel(1, 255, 0, 0)
  else:
    n.set_pixel(1, 0, 0, 0)

  if quokka.button_c.is_pressed():
    quokka.display.print('c')
    n.set_pixel(2, 255, 0, 0)
  else:
    n.set_pixel(2, 0, 0, 0)

  if quokka.button_d.is_pressed():
    quokka.display.print('d')
    n.set_pixel(3, 255, 0, 0)
  else:
    n.set_pixel(3, 0, 0, 0)

  if quokka.button_usr.is_pressed():
    quokka.display.print('u')
    n.set_pixel(4, 255, 0, 0)
  else:
    n.set_pixel(4, 0, 0, 0)

  n.show()
  quokka.display.show()
  quokka.sleep(50)
