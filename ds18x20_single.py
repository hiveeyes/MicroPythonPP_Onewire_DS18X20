#
# Convenience adapter class for reading a single
# DS18X20 temperature sensor attached to the 1-Wire bus.
#
from ds18x20 import DS18X20


class DS18X20Single(DS18X20):

    def start_conversion(self, rom=None):
        if (rom is None) and (len(self.roms) == 1):
            rom = self.roms[0]
        return super().start_conversion(rom)

    def read_temp_async(self, rom=None):
        if (rom is None) and (len(self.roms) == 1):
            rom = self.roms[0]
        return super().read_temp_async(rom)
