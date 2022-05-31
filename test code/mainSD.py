import os
from machine import Pin, SoftSPI
from sdcard import SDCard

spisd = SoftSPI(-1,
                miso=Pin(13),
                mosi=Pin(12),
                sck=Pin(14))
sd = SDCard(spisd, Pin(27))

print('Directory: {}'.format(os.listdir()))
vfs=os.VfsFat(sd)
os.mount(vfs, '/sd')
print('Directory: {}'.format(os.listdir()))
os.chdir('sd')
print('Directory SD: {}'.format(os.listdir()))

