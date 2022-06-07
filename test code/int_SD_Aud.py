
from machine import I2S
from machine import Pin
from time import sleep_ms
import os
from machine import Pin, SoftSPI
from sdcard import SDCard

spisd = SoftSPI(-1,
                miso=Pin(13),
                mosi=Pin(12),
                sck=Pin(14))
sd = SDCard(spisd, Pin(27))

vfs=os.VfsFat(sd)
os.mount(vfs, '/sd')

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

# ---------------------------------------------------------

WAV_FILE = 'taunt-16k-16bits-mono-12db.wav' 
wav_file = '/sd/{}'.format(WAV_FILE)
wav = open(wav_file,'rb')

wav_len = wav.seek(0, 2)
print(wav_len)
pos = wav.seek(44)

wav_samples = bytearray(1024)
wav_samples_mv = memoryview(wav_samples)

while  pos < wav_len:
    num_written = audio_out.write(wav_samples_mv)
    pos += num_written
    wav.seek(pos)
    wav.readinto(wav_samples_mv)
    
print("Fin del audio.")
