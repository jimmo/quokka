import machine
import quokka
import sys

quokka.display.fill(1)
quokka.display.text('radio', 5, 5, 0)
quokka.display.show()

v = quokka.radio.version()
if not v:
  sys.exit(0)

quokka.display.text('version:' + v, 5, 20, 0)

quokka.radio.on()

quokka.radio.config(channel=22)

while True:
  msg = quokka.radio.receive()
  if msg:
    quokka.display.fill(1)
    quokka.display.text(msg, 5, 5, 0)
    quokka.display.show()
  if quokka.buttons.a.was_pressed():
    quokka.radio.send('a')
  if quokka.buttons.b.was_pressed():
    quokka.radio.send('b')
