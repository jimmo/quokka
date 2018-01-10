import quokka

while True:
  for i in range(4):
    if quokka.buttons.all[i].is_pressed():
      quokka.leds.all[i].on()
    else:
      quokka.leds.all[i].off()

  quokka.sleep(50)
