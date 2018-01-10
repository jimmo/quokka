import machine
import quokka

quokka.display.fill(1)
quokka.display.text('radio', 5, 5, 0)
quokka.display.show()

quokka.radio.enable()
print('version:', quokka.radio.version())

quokka.radio.config(channel=22)

while True:
  msg = quokka.radio.receive()
  if msg:
    quokka.display.fill(1)
    quokka.display.text(msg, 5, 5, 0)
    quokka.display.show()
  if quokka.buttons.a.was_pressed():
    quokka.radio.send('a')
