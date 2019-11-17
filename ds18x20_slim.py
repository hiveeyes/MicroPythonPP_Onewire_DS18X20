# DS18x20 temperature sensor driver for MicroPython.
# MIT license; Copyright (c) 2016 Damien P. George

from micropython import const

_CONVERT = const(0x44)
_RD_SCRATCH = const(0xbe)
_WR_SCRATCH = const(0x4e)

class DS18X20:
    def __init__(self, onewire):
        self.ow = onewire
        self.buf = bytearray(9)
        self.roms = self.scan()

    def scan(self):
        return [rom for rom in self.ow.scan() if rom[0] in (0x10, 0x22, 0x28)]

    def convert_temp(self):
        self.ow.reset()
        self.ow.write_byte(self.ow.CMD_SKIPROM)
        self.ow.write_byte(_CONVERT)

    def read_scratch(self, rom):
        self.ow.reset()
        self.ow.select_rom(rom)
        self.ow.write_byte(_RD_SCRATCH)
        self.ow.read_into(self.buf)
        assert self.ow.crc8(self.buf) == 0, 'CRC error'
        return self.buf

    def write_scratch(self, rom, buf):
        self.ow.reset()
        self.ow.select_rom(rom)
        self.ow.write_byte(_WR_SCRATCH)
        self.ow.write_bytes(buf)

    def read_temp(self, rom):
        try:
            buf = self.read_scratch(rom)
            if rom[0] == 0x10:
                if buf[1]:
                    t = buf[0] >> 1 | 0x80
                    t = -((~t + 1) & 0xff)
                else:
                    t = buf[0] >> 1
                return t - 0.25 + (buf[7] - buf[6]) / buf[7]
            else:
                t = buf[1] << 8 | buf[0]
                if t & 0x8000: # sign bit set
                    t = -((t ^ 0xffff) + 1)
            return t / 16
        except AssertionError:
            return None
