import quokka

while True:
  quokka.display.fill(0)
  if quokka.buttons.a.is_pressed():
    quokka.display.text('a', 5, 5, 1)
  if quokka.buttons.b.is_pressed():
    quokka.display.text('b', 20, 5, 1)
  if quokka.buttons.c.is_pressed():
    quokka.display.text('c', 35, 5, 1)
  if quokka.buttons.d.is_pressed():
    quokka.display.text('d', 50, 5, 1)
  if quokka.buttons.usr.is_pressed():
    quokka.display.text('u', 65, 5, 1)
  quokka.display.show()
  quokka.sleep(50)
