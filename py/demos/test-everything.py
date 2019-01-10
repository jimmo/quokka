import quokka
import neopixel
import radio

n = neopixel.NeoPixel()

quokka.display.print('radio fw', radio.version())
quokka.sleep(1000)
n.clear()
n.show()


radio.config(channel=22)
radio.on()

next_accel = 0


while True:
  if quokka.button_a.was_pressed():
    quokka.display.print('a')
    quokka.red.toggle()
    radio.send('a')

  if quokka.button_b.was_pressed():
    quokka.display.print('b')
    quokka.blue.toggle()
    radio.send('b')

  if quokka.button_c.was_pressed():
    quokka.display.print('c')
    quokka.orange.toggle()
    radio.send('c')

  if quokka.button_d.was_pressed():
    quokka.display.print('d')
    quokka.green.toggle()
    radio.send('d')

  if quokka.button_usr.was_pressed():
    quokka.display.print('u')
    radio.send('u')

  if quokka.button_a.is_pressed():
    n.set_pixel(0, 255, 0, 0)
  else:
    n.set_pixel(0, 0, 0, 0)

  if quokka.button_b.is_pressed():
    n.set_pixel(1, 255, 0, 0)
  else:
    n.set_pixel(1, 0, 0, 0)

  if quokka.button_c.is_pressed():
    n.set_pixel(2, 255, 0, 0)
  else:
    n.set_pixel(2, 0, 0, 0)

  if quokka.button_d.is_pressed():
    n.set_pixel(3, 255, 0, 0)
  else:
    n.set_pixel(3, 0, 0, 0)

  if quokka.button_usr.is_pressed():
    n.set_pixel(4, 255, 0, 0)
  else:
    n.set_pixel(4, 0, 0, 0)

  msg = radio.receive()
  if msg:
    quokka.display.print(msg)

  if quokka.running_time() > next_accel:
    quokka.display.print(quokka.accelerometer.get_values())
    next_accel = quokka.running_time() + 2000

  n.show()
  quokka.sleep(50)
