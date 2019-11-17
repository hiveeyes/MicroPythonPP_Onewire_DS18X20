import time
from machine import Pin
from ds18x20_new import DS18X20
from onewire_new import OneWire

#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)

temp.convert_temp()
while True:
    time.sleep(1)
    for rom in temp.roms:
        print(temp.read_temp(rom), end=" ")
    print()
    temp.convert_temp()

