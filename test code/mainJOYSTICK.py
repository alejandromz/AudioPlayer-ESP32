from machine import Pin, ADC
from time import sleep_ms

x = ADC(Pin(34))
y = ADC(Pin(35))

x.atten(ADC.ATTN_11DB)
y.atten(ADC.ATTN_11DB)

sw = Pin(26, Pin.IN, Pin.PULL_UP)

while True:
    x_val = x.read()
    y_val = y.read()
    print("Current_position:{},{}".format(x_val,y_val))
    print('Pin_Value=',sw.value())
    sleep_ms(300)
    
    
    
#     y_val = y.read()
#     print("x_position:",x_val)
#     sleep(0.1)
