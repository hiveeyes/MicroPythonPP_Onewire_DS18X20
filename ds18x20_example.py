import time
from machine import Pin
from ds18x20 import DS18X20
from onewire import OneWire

#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)

while True:
    for rom in temp.roms:
        temp.start_conversion(rom)
        time.sleep(1)
        print(temp.read_temp_async(rom), end=" ")
    print()
    time.sleep(1)
