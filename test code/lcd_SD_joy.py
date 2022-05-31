from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from i2c_lcd import I2cLcd
from machine import Pin, ADC, SoftSPI
from time import sleep_ms
from sdcard import SDCard
import os

x = ADC(Pin(34))
y = ADC(Pin(35))

x.atten(ADC.ATTN_11DB)
y.atten(ADC.ATTN_11DB)

sw = Pin(26, Pin.IN, Pin.PULL_UP)

DEFAULT_I2C_ADDR = 0X27

i2c=I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR,2,16)

spisd = SoftSPI(-1,
                miso=Pin(13),
                mosi=Pin(12),
                sck=Pin(14))
sd = SDCard(spisd, Pin(27))
vfs=os.VfsFat(sd)
os.mount(vfs, '/sd')
os.chdir('sd')


threshold = 500
directorio = os.listdir()
directorio = [st[0:12] for st in directorio]
    
pos = 0

lcd.clear()
lcd.putstr('{}\n{}'.format(directorio[pos],directorio[pos+1]))

while True:
    x_val = x.read()
    y_val = y.read()
    if y_val < threshold:
        pos = pos-1
        if pos<0:
            pos=0
    elif y_val > 4095-threshold:
        pos = pos+1
        if pos>len(directorio)-1:
            pos = len(directorio)-1
    ## print("Current_position:{},{}".format(x_val,y_val))
    ## print('Pin_Value=',sw.value())
    lcd.clear()
    if pos == len(directorio)-1:
        lcd.putstr('{}\n>{}'.format(directorio[pos-1],directorio[pos]))
    else:
        lcd.putstr('>{}\n{}'.format(directorio[pos],directorio[pos+1]))
    sleep_ms(300)
    