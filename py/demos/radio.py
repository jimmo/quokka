import machine

spi = machine.SPI('Y', baudrate=10000000)


import ssd1306
disp_slave_select = machine.Pin('Y5', machine.Pin.OUT)
disp_slave_select.value(1)
d = ssd1306.SSD1306_SPI(128, 64, spi, machine.Pin('X11'), machine.Pin('X22'), disp_slave_select)

import quokka_radio
nrf_slave_select = machine.Pin('Y4', machine.Pin.OUT)
nrf_slave_select.value(1)
r = quokka_radio.Radio(nrf_slave_select, spi)

d.fill(1)
d.text('radio', 5, 5, 0)
d.show()

r.enable()
print('version:', r.version())
print('version:', r.version())

import pyb
pyb.LED(2).on()

r.set_channel(22)

while True:
    msg = r.receive()
    if msg:
        d.fill(1)
        d.text(msg, 5, 5, 0)
        d.show()
