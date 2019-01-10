import quokka
import time

x = 32
y = 0
dx = -1
dy = -1

q = quokka.Image.load('quokka-46x64.qimz')
while True:
  quokka.display.fill(1)
  quokka.display.scale_blit(q, x, y, 2, 1)
  quokka.display.show()
  if x == 127 - 23 or x == -23:
    dx = -dx
  if y == 63 - 32 or y == -32:
    dy = -dy
  x += dx
  y += dy
  
