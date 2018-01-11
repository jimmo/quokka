import quokka

quokka.display.fill(0)
quokka.display.text(quokka.radio.version(), 0, 0, 1)
quokka.display.show()
quokka.sleep(1000)

while True:
  quokka.display.fill(0)
  quokka.neopixels.clear()
  if quokka.buttons.a.is_pressed():
    quokka.display.text('a', 5, 5, 1)
    quokka.neopixels.set_pixel(0, 255, 0, 0)
  if quokka.buttons.b.is_pressed():
    quokka.display.text('b', 20, 5, 1)
    quokka.neopixels.set_pixel(1, 255, 0, 0)
  if quokka.buttons.c.is_pressed():
    quokka.display.text('c', 35, 5, 1)
    quokka.neopixels.set_pixel(2, 255, 0, 0)
  if quokka.buttons.d.is_pressed():
    quokka.display.text('d', 50, 5, 1)
    quokka.neopixels.set_pixel(3, 255, 0, 0)
  if quokka.buttons.usr.is_pressed():
    quokka.display.text('u', 65, 5, 1)
  quokka.display.show()
  quokka.sleep(50)
