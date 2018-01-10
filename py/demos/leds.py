import quokka
import time

while True:
  for i in range(4):
    quokka.leds.all[i % 4].on()
    quokka.leds.all[(i + 3) % 4].off()
    time.sleep_ms(500)
