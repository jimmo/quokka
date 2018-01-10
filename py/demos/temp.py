import quokka

while True:
  quokka.display.fill(0)
  quokka.display.text(str(quokka.temperature()), 10, 10, 1)
  quokka.display.show()
  quokka.sleep(500)
