from machine import I2S
from machine import Pin
from time import sleep_ms


bck_pin = Pin(22)   # Pin BCLK
ws_pin = Pin(21)    # Pin LRC
sdout_pin = Pin(23) # Pin Din

audio_out = I2S(1,
                sck=bck_pin, ws=ws_pin, sd=sdout_pin,
                mode=I2S.TX, 
                bits=16, 
                format=I2S.MONO,
                rate=16000,
                ibuf=2000)
               
samples = bytearray([1,0,1,0,0,0,1,1,1,1,0,1,1,0]*100)

while True:
    num_bytes_written = audio_out.write(samples)
    sleep_ms(100)
