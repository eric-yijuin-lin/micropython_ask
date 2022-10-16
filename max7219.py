from machine import Pin, SPI
import time

DECODEMODE = const(9)
INTENSITY = const(10) #0xA
SCANLIMIT = const(11) #0xB
SHUTDOWN = const(12)  #0xC
DISPLAYTEST = const(15) #0xF

sprite = ( 
    (0x00, 0x0C, 0x12, 0x24, 0x24, 0x12, 0x0C, 0x00),
    (0x1C, 0x22, 0x42, 0x84, 0x84, 0x42, 0x22, 0x1C),
    (0x00, 0x0C, 0x12, 0x24, 0x24, 0x12, 0x0C, 0x00),
    (0x1C, 0x22, 0x42, 0x84, 0x84, 0x42, 0x22, 0x1C),
)

cs = Pin(5, Pin.OUT)
spi = SPI(1, 
    baudrate=10000000, 
    polarity=1, 
    phase=0, 
    sck=Pin(18, Pin.OUT), 
    mosi=Pin(23, Pin.OUT)
)

def max7219(reg, data):
    cs.value(0)
    spi.write(bytes([reg, data]))
    cs.value(1)

def init():
    for reg, data in (
        (DISPLAYTEST, 0),
        (SCANLIMIT, 7),
        (INTENSITY, 1),
        (DECODEMODE, 0),
        (SHUTDOWN, 1)
    ):
        max7219(reg, data)

def clear():
    for i in range(8):
        max7219(i + 1, 0)

def show():
    print('showing')
    for i in range(4):
        for j in range(8):
            max7219(j+1, sprite[i][j])
        time.sleep(0.3)

try:
    init()
    while True:
        show()  
except:
    clear()
