
import quokka

while True:
  for i in range(4):
    if quokka.buttons[i].is_pressed():
      quokka.leds[i].on()
    else:
      quokka.leds[i].off()

  quokka.sleep(50)
