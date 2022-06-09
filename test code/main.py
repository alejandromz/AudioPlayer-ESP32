## ---------------------------------------------
# 
# Project: ESP32 Audio Player
# Universidad Nacional de Colombia - Sede Bogotá
# Departamento de Ingeniería Eléctrica y Electrónica
#
# Sistemas Embebidos 2022-1
# Professor: Johnny German Cubides Castro
# 
## ---------------------------------------------

# Import required libraries
from time import sleep_ms, ticks_ms
from machine import I2C, I2S, Pin, ADC, SoftSPI
from i2c_lcd import I2cLcd
from sdcard import SDCard
import os


## Allocate buffer variables
wav_samples = bytearray(1024)
wav_samples_mv = memoryview(wav_samples)


## Define functions
def display_menu(directorio, pos):
    lcd.clear()
    if pos == len(directorio)-1:
        lcd.putstr('{}\n>{}'.format(directorio_dsp[pos-1],directorio_dsp[pos]))
    else:
        lcd.putstr('>{}\n{}'.format(directorio_dsp[pos],directorio_dsp[pos+1]))
    sleep_ms(300)
    

def navigate(pos):
    y_val = y.read()
    if y_val < threshold:
        pos = pos-1
        if pos<0:
            pos=0
    elif y_val > 4095-threshold:
        pos = pos+1
        if pos>len(directorio)-1:
            pos = len(directorio)-1
    return pos
        

def select_dir(directorio, old_dir, pos, state):
    wav = None
    if directorio[pos] == 'Return':
        try:
            lst = old_dir.split('/')
            old_dir=''
            
            if (len(lst) > 2 and lst[0] != '') or len(lst) > 3:
                for item in lst[0:-2]:
                    ## print(item)
                    if item != '':
                        old_dir=old_dir+'/'+item
            else:
                old_dir=owd
        except:
            print('Error')
                
        os.chdir(old_dir)
        directorio = os.listdir()
        if old_dir != owd:
            directorio.append('Return')
        pos = 0
    elif directorio[pos][-4:] == '.wav':
        state = 'play'
        wav_file = old_dir+directorio[pos]
        wav = open(wav_file,'rb')
    else:
        try:
            os.chdir(directorio[pos])
            old_dir=old_dir+directorio[pos]+'/'
            directorio = os.listdir()
            directorio.append('Return')
            pos = 0
        except:
            print('No es un directorio.')
    return directorio, old_dir, pos, state, wav


def play_wav(wav, w_pos, wav_len, state):
    global wav_samples_mv
    if  w_pos < wav_len:
        wav.seek(w_pos)
        wav.readinto(wav_samples_mv)
        num_written = audio_out.write(wav_samples_mv)
        w_pos += num_written
    else:
        state = 'pause'
        w_pos = wav.seek(44)
    return w_pos, state
            
            
def display_wav(directorio, pos, w_pos, wav_len, state):
    lcd.clear()
    lcd.putstr('{}\n{}'.format(directorio[pos][:12], state))
    
    
def play_pause(state):
    if sw.value()==0:
        if state == 'play':
            state = 'pause'
        elif state == 'pause':
            state='play'
        sleep_ms(200)
        
    x_val = x.read()
    if x_val < threshold:
        state = 'menu'
        wav.close()
        
    return state
        
        
## Initialize class instances

# Initialize SDCard object
spisd = SoftSPI(-1,
                miso=Pin(21),
                mosi=Pin(19),
                sck=Pin(18))
sd = SDCard(spisd, Pin(5))

# Initialize I2S object
# sck=Pin(16), ws=Pin(17), sd=Pin(4),
audio_out = I2S(1,
                sck=Pin(25), ws=Pin(26), sd=Pin(4),
                mode=I2S.TX,
                bits=16, 
                format=I2S.MONO,
                rate=16000,
                ibuf=2000)

# Initialize I2C object
DEFAULT_I2C_ADDR = 0X27
# i2c=I2C(scl=Pin(22), sda=Pin(21), freq=400000)
i2c=I2C(scl=Pin(22), sda=Pin(15), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR,2,16)

# Initialize joystick
threshold = 500
x = ADC(Pin(32))
y = ADC(Pin(33))
x.atten(ADC.ATTN_11DB)
y.atten(ADC.ATTN_11DB)
sw = Pin(14, Pin.IN, Pin.PULL_UP)


## Initialize SD storage 
vfs=os.VfsFat(sd)
os.mount(vfs, '/sd')
owd = os.getcwd()
old_dir=owd


## Create list of the sd directories
directorio = os.listdir()
directorio_dsp = [st[0:12] for st in directorio]
pos = 0
display_menu(directorio, pos)


## Define initial state
state = 'menu'
wav = None
wav_len = 0
w_pos = 0


## Main loop
while True:
    if state == 'menu':
        old_pos = pos
        pos = navigate(old_pos)
        if pos != old_pos:
            display_menu(directorio, pos)
            sleep_ms(100)
            
        if sw.value()==0:
            directorio, old_dir, pos, state, wav = select_dir(directorio, old_dir, pos, state)
            directorio_dsp = [st[0:12] for st in directorio]
            if state == 'play':
                wav_len = wav.seek(0, 2)
                w_pos = wav.seek(44)
                display_wav(directorio, pos, w_pos, wav_len, state)
            else:
                display_menu(directorio, pos)
            sleep_ms(200)
    elif state == 'play':
        w_pos, state = play_wav(wav, w_pos, wav_len, state)
        state = play_pause(state)
        if state == 'pause':
            display_wav(directorio, pos, w_pos, wav_len, state)
        elif state == 'menu':
            display_menu(directorio, pos)
    elif state == 'pause':
        state = play_pause(state)
        if state == 'play':
            display_wav(directorio, pos, w_pos, wav_len, state)
        elif state == 'menu':
            display_menu(directorio, pos)
    else:
        print('State errror.')
            
    
    