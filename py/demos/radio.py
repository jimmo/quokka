import machine
import quokka
import sys

quokka.display.print('radio')

import radio
v = radio.version()
if not v:
  quokka.display.print('bad radio')
  quokka.display.show()
  sys.exit(0)

quokka.display.print('version: ' + v)

radio.on()

radio.config(channel=22)

while True:
  msg = radio.receive()
  if msg:
    quokka.display.clear()
    quokka.display.print(msg)
  if quokka.buttons.a.was_pressed():
    radio.send('a')
  if quokka.buttons.b.was_pressed():
    radio.send('b')
