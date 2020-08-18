import spidev
from time import sleep

m31855 = spidev.SpiDev(0,1)
m31855.max_speed_hz=1000000

def c_to_f(temp):
    f = ((temp/5)*9)+32
    return f

def readTempC():
    m31855.writebytes([0x00,0x00,0x00,0x00])
    tempRead = m31855.readbytes(4)
    print(tempRead)
    temp32 = tempRead[0] <<24 | tempRead[1] <<16 | tempRead[2] <<8 | tempRead[3]
    internal = (temp32 >> 4) & 0x7ff
    if temp32 & 0x800:
        internal = internal - 4096
    internal = internal * 0.0625
    if temp32 & 0x7:
        temp = float('NaN')
    if temp32 & 0x80000000:
        temp = temp32 >> 18
        temp = temp - 16384
    else:
        temp = temp32 >> 18
    temp = temp * 0.25
    return temp, internal

while True:
    temp, internal = readTempC()
    print('Thermocouple Temperature: {0:0.3F}°C / {1:0.3F}°F'.format(temp, c_to_f(temp)))
    print('    Internal Temperature: {0:0.3F}°C / {1:0.3F}°F'.format(internal, c_to_f(internal)))
    sleep(2)
