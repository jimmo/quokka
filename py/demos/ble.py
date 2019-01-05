import time
import quokka

quokka.radio.ble_on()
for i in range(10):
    quokka.radio.ble_adv([(0x01, b'\x06'), (0x09, b'Quokka%u' % i)])
    time.sleep(6)
quokka.radio.ble_off()
