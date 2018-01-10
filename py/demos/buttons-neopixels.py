import quokka

while True:
  quokka.neopixels.clear()
  for i, b in enumerate(quokka.buttons.all):
    quokka.neopixels.set_pixel(i, 255 if b.is_pressed() else 0, 0, 0)
  if quokka.buttons.usr.is_pressed():
    for i in range(4, 8):
      quokka.neopixels.set_pixel_rainbow(i, (i-4) * 30, 255)
  quokka.neopixels.show()

  quokka.sleep(50)
