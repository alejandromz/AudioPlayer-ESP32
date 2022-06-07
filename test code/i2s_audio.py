from machine import I2S
from machine import Pin
from time import sleep_ms


bck_pin = Pin(22)   # Pin BCLK
ws_pin = Pin(21)    # Pin LRC
sdout_pin = Pin(23) # Pin Din

audio_out = I2S(1,                                  # create I2S peripheral to write audio
                sck=bck_pin, ws=ws_pin, sd=sdout_pin,   # sample data to an Adafruit I2S Amplifier
                mode=I2S.TX,  # breakout board, 
                bits=16,                        # based on MAX98357A device
                format=I2S.MONO,
                rate=16000,
                ibuf=2000)
               
samples = bytearray([1,0,1,0,0,0,1,1,1,1,0,1,1,0]*100)                                 # bytearray containing audio samples to transmit

while True:
    num_bytes_written = audio_out.write(samples)
    sleep_ms(100)