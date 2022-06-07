
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

# print('Directory: {}'.format(os.listdir()))
vfs=os.VfsFat(sd)
os.mount(vfs, '/sd')
# os.chdir('sd')
# print('Directory: {}'.format(os.listdir()))

WAV_FILE = 'taunt-16k-16bits-mono-12db.wav'
# WAV_FILE = 'PRUEBADJ.wav'

# ----------------------------------------------------------------------------

bck_pin = Pin(22)   # Pin BCLK
ws_pin = Pin(21)    # Pin LRC
sdout_pin = Pin(23) # Pin Din

audio_out = I2S(1,                                  # create I2S peripheral to write audio
                sck=bck_pin, ws=ws_pin, sd=sdout_pin,   # sample data to an Adafruit I2S Amplifier
                mode=I2S.TX,  # breakout board, 
                bits=16,                        # based on MAX98357A device
                format=I2S.MONO,
                rate=16000,
                # rate=1411000,
                ibuf=2000)
 
wav_file = '/sd/{}'.format(WAV_FILE)
wav = open(wav_file,'rb')

wav_len = wav.seek(0, 2)
print(wav_len)
pos = wav.seek(44)

wav_samples = bytearray(1024)
wav_samples_mv = memoryview(wav_samples)

num_read = wav.readinto(wav_samples_mv)
num_written = num_read
num_pos = 0
while  pos < wav_len:
    num_written = audio_out.write(wav_samples_mv)
    pos += num_written
    wav.seek(pos)
    wav.readinto(wav_samples_mv)
    
print("C'est fini")
