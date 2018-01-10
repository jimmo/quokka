from pyb import delay, udelay, millis
from machine import Pin, SPI


SPI_STATE_ON = 0x01
SPI_STATE_OFF = 0x00
SPI_QUERY = 0x02


SPI_RADIO_STATE = 0x01 << 2
SPI_RADIO_CHAN = 0x02 << 2
SPI_RADIO_POWER = 0x03 << 2
SPI_MSG_AVAIL = 0x04 << 2
SPI_SEND_MSG = 0x05 << 2
SPI_RECV_MSG = 0x06 << 2


SPI_NOOP = 0x00
SPI_VERSION = SPI_QUERY

SPI_RADIO_STATE_DISABLE = SPI_RADIO_STATE | SPI_STATE_OFF
SPI_RADIO_STATE_ENABLE = SPI_RADIO_STATE | SPI_STATE_ON
SPI_RADIO_STATE_QUERY = SPI_RADIO_STATE | SPI_QUERY

SPI_RADIO_CHAN_SET = SPI_RADIO_CHAN
SPI_RADIO_CHAN_QUERY = SPI_RADIO_CHAN | SPI_QUERY

SPI_RADIO_POWER_SET = SPI_RADIO_POWER
SPI_RADIO_POWER_QUERY = SPI_RADIO_POWER | SPI_QUERY

SPI_MSG_QUERY = SPI_MSG_AVAIL | SPI_QUERY

SPI_SEND_CMD = SPI_SEND_MSG
SPI_RECV_CMD = SPI_RECV_MSG


SPI_NOCMD = 0x00
SPI_SUCCESS = 0x01
SPI_OUT_OF_RANGE = 0x02
SPI_SUCCESS_AND_ENABLED = 0x03
SPI_SUCCESS_AND_DISABLED = 0x04
SPI_INVALID_LENGTH = 0x05
SPI_REPLY_OVERFLOW = 0x06
SPI_CHECKSUM_FAIL = 0x07
SPI_INVALID_COMMAND = 0x08
SPI_NO_MESSAGE = 0x10
SPI_MESSAGE = 0x11
SPI_PERIPH_BUSY = 0xF0
SPI_OVERFLOW = 0xF1
SPI_OTHER_FAIL = 0xFF


class RadioError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class QuokkaRadio:
    def __init__(self, slave_select, spi):
        self.slave_select = slave_select
        self.spi = spi

        time = millis() + 1000
        success = False
        while millis() < time:
            try:
                self.version()
            except RadioError:
                continue
            success = True
            break
        if success == False:
            raise RadioError("Radio comm")

    def version(self):
        response = self._write([SPI_VERSION])
        return bytes(self.read_packet(response)).decode('ascii').strip('\x00')

    def enable(self):
        self._write([SPI_RADIO_STATE_ENABLE])

    def disable(self):
        self._write([SPI_RADIO_STATE_DISABLE])

    def is_enabled(self):
        response = self._write([SPI_RADIO_STATE_QUERY])
        if response[0] == SPI_SUCCESS_AND_ENABLED:
            return True
        elif response[0] == SPI_SUCCESS_AND_DISABLED:
            return False
        return False

    def config(self, channel=0, power=6):
        if not 0 <= channel <= 100:
            raise ValueError("Invalid channel")
        if not 0 <= power <= 7:
            raise ValueError('Invalid power')
        self._write([SPI_RADIO_CHAN_SET, 1, channel & 0xff, channel & 0xff])
        self._write([SPI_RADIO_POWER_SET, 1, power, power])

    def get_channel(self):
        response = self._write([SPI_RADIO_CHAN_QUERY])
        return self.read_packet(response)[0]

    def get_power(self):
        response = self._write([SPI_RADIO_POWER_QUERY])
        return self.read_packet(response)[0]

    def is_message_available(self):
        response = self._write([SPI_MSG_QUERY])
        if response[0] == SPI_MESSAGE:
            return True
        elif response[0] == SPI_NO_MESSAGE:
            return False
        return False

    def send(self, message):
        message = bytearray(message)
        chk = 0
        for c in message:
            chk ^= c


        self._write([SPI_SEND_CMD, len(message)] + list(message) + [chk])

    def receive(self):
        r = self._write([SPI_RECV_CMD])
        data = self.read_packet(r)
        if data is not None:
            return bytes(data).decode()
        return data

    def _write(self, data):
        data = bytearray(data)
        resp = bytearray(len(data))

        self.slave_select.value(0)
        self.spi.write_readinto(data, resp)
        while resp[0] == SPI_PERIPH_BUSY:
            self.slave_select.value(1)
            udelay(100)
            self.slave_select.value(0)
            self.spi.write_readinto(data, resp)
        self.slave_select.value(1)

        self.slave_select.value(0)
        resp = self.spi.read(1, 0x00)[0]
        while resp == SPI_PERIPH_BUSY:
            self.slave_select.value(1)
            udelay(100)
            self.slave_select.value(0)
            resp = self.spi.read(1, 0x00)[0]

        data = bytearray(64)
        self.spi.readinto(data, 0x00)
        self.slave_select.value(1)

        data[1:] = data[:-1]
        data[0] = resp

        return data

    def read_packet(self, packet):
        status_code = packet[0]
        if status_code not in (SPI_SUCCESS, SPI_SUCCESS_AND_ENABLED, SPI_SUCCESS_AND_DISABLED, SPI_NO_MESSAGE):
            raise RadioError("error code 0x%x" % status_code)

        if status_code == SPI_NO_MESSAGE:
            return None

        length = packet[1]
        if length == 0:
            return bytearray()
        data = packet[2:(2 + length)]
        expected_checksum = packet[2 + length]


        checksum = 0
        for d in data:
            checksum ^= d
        if checksum != expected_checksum:
            raise RadioError('xs (a %d, e %d)' % (checksum, expected_checksum))

        return data
