#!/usr/bin/env python3.7
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
 
import time
import math
from rpi_ws281x import *
from guizero import App, Text, PushButton, Box, CheckBox, Combo, ButtonGroup, Slider
import argparse
import threading
#import multiprocessing 

# LED strip configuration:
LED_COUNT      = 240     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        if leds[i] == True:
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms/1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def setAll(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)

def allBarsOn(strip, color):
    """Turn all bars on"""
    setAll(strip, color)
    strip.show()

def selectedBarsOn(strip, color):
    """Turn selected bars on other off"""
    for i in range(strip.numPixels()):
        if leds[i] == True:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def allBarsOff(strip):
    """Turn all bars off"""
    setAll(strip, Color(0, 0, 0))
    strip.show()

def FadeIn(strip):
    global r,g,b
    for i in range (0, 256):
        if bar_4_sel.value == 1:
            for x in range(0, 15):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_3_sel.value == 1:
            for x in range(15, 30):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_2_sel.value == 1:
            for x in range(30, 45):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_1_sel.value == 1:
            for x in range(45, 60):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_5_sel.value == 1:
            for x in range(60, 101):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()
        
        if bar_6_sel.value == 1:
            for x in range(101, 144):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_7_sel.value == 1:
            for x in range(144, 185):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_8_sel.value == 1:
            for x in range(185, 227):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

def FadeOut(strip):
    global r,g,b
    for i in range (256, 0, -1):
        if bar_4_sel.value == 1:
            for x in range(0, 15):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_3_sel.value == 1:
            for x in range(15, 30):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_2_sel.value == 1:
            for x in range(30, 45):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_1_sel.value == 1:
            for x in range(45, 60):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_5_sel.value == 1:
            for x in range(60, 101):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()
        
        if bar_6_sel.value == 1:
            for x in range(101, 144):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_7_sel.value == 1:
            for x in range(144, 185):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

        if bar_8_sel.value == 1:
            for x in range(185, 227):
                red = int(math.floor((i / 256.0) * r))
                green = int(math.floor((i / 256.0) * g))
                blue = int(math.floor((i / 256.0) * b))
                strip.setPixelColor(x, Color(red,green,blue))
            strip.show()

def RunningLights(strip, WaveDelay=20):
    global r, g, b
    red = r
    green = g
    blue = b
    Position=0
    for i in range (0, (LED_COUNT * 2)):
        Position = Position + 1
        for i in range (0, LED_COUNT):
            strip.setPixelColor(i, Color(int(math.floor(((math.sin(i+Position) * 127 + 128) / 255) * red)), int(math.floor(((math.sin(i+Position) * 127 + 128) / 255) * green)), int(math.floor(((math.sin(i+Position) * 127 + 128) / 255) * blue))))
        strip.show()
        time.sleep(WaveDelay/1000)

def flashBar1(strip, color, speed=50):
    # Off
    for i in range(45, 60):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(45, 60):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(45, 60):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashBar2(strip, color, speed=50):
    # Off
    for i in range(30, 45):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(30, 45):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(30, 45):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashBar3(strip, color, speed=50):
    # Off
    for i in range(15, 30):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(15, 30):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(15, 30):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashBar4(strip, color, speed=50):
    # Off
    for i in range(0, 15):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(0, 15):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(0, 15):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashBar5(strip, color, speed=50):
    # Off
    for i in range(60, 101):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(60, 101):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(60, 101):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashBar6(strip, color, speed=50):
    # Off
    for i in range(101, 144):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(101, 144):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(101, 144):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashBar7(strip, color, speed=50):
    # Off
    for i in range(144, 185):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(144, 185):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(144, 185):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashBar8(strip, color, speed=50):
    # Off
    for i in range(185, 227):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(185, 227):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(185, 227):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashAll(strip, color, speed=50):
    """Flash all bars"""
    setAll(strip, Color(0, 0, 0))
    strip.show()

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)

    setAll(strip, Color(0, 0, 0))
    strip.show()

def flashSmallSquare(strip, color, speed=50):
    """Flash small square"""
    # Off
    for i in range(0, 60):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(0, 60):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(0, 60):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashBigSquare(strip, color, speed=50):
    """Flash big square"""
    # Off
    for i in range(60, 227):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    #On
    for i in range(60, 227):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)
    #Off
    for i in range(60, 227):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def flashSelected(strip, color, speed=50):
    """Flash selected bars"""
    setAll(strip, Color(0, 0, 0))
    strip.show()
    
    for i in range(strip.numPixels()):
        if leds[i] == True:
            strip.setPixelColor(i, color)
    strip.show()
    time.sleep(speed/1000.0)

    setAll(strip, Color(0, 0, 0))
    strip.show()

# Global variables
r = 0
g = 0
b = 0
leds = []

def go_red():
    global r, g, b
    r = 255
    g = 0
    b = 0

def go_green():
    global r, g, b
    r = 0
    g = 255
    b = 0

def go_blue():
    global r, g, b
    r = 0
    g = 0
    b = 255

def go_white():
    global r, g, b
    r = 255
    g = 255
    b = 255

def update_color():
    if color_radio.value == "Red":
        go_red()
        color_text.value = "Red is selected"
        color_text.text_color = "red"
    elif color_radio.value == "Blue":
        go_blue()
        color_text.value = "Blue is selected"
        color_text.text_color = "blue"
    elif color_radio.value == "Green":
        go_green()
        color_text.value = "Green is selected"
        color_text.text_color= "green"
    else:
        go_white()
        color_text.value = "White is selected"
        color_text.text_color = "white"

def update_bar_selection():
    for index, value in enumerate(leds):
        if index < 15:
            if bar_4_sel.value == 1:
                leds[index] = True
            else:
                leds[index] = False
        elif index >= 15 and index < 30:
            if bar_3_sel.value == 1:
                leds[index] = True
            else:
                leds[index] = False
        elif index >= 30 and index < 45:
            if bar_2_sel.value == 1:
                leds[index] = True
            else:
                leds[index] = False
        elif index >= 45 and index < 60:
            if bar_1_sel.value == 1:
                leds[index] = True
            else:
                leds[index] = False
        elif index >= 60 and index < 101:
            if bar_5_sel.value == 1:
                leds[index] = True
            else:
                leds[index] = False
        elif index >= 101 and index < 144:
            if bar_6_sel.value == 1:
                leds[index] = True
            else:
                leds[index] = False
        elif index >= 144 and index < 185:
            if bar_7_sel.value == 1:
                leds[index] = True
            else:
                leds[index] = False
        elif index >= 185 and index < 227:
            if bar_8_sel.value == 1:
                leds[index] = True
            else:
                leds[index] = False

StrobeCount = 0
FlashDelay = 0
EndPause = 0

def update_strobe_count(slider_value):
    global StrobeCount
    StrobeCount = int(slider_value)

def update_flash_delay(slider_value):
    global FlashDelay
    FlashDelay = float(slider_value) * 10

def update_endpause_count(slider_value):
    global EndPause
    EndPause = float(slider_value) * 10

def Strobe(strip):
    global r, g, b, StrobeCount, FlashDelay, EndPause
    for i in range (0, StrobeCount):
        for x in range(strip.numPixels()):
            if leds[x] == True:
                strip.setPixelColor(x, Color(r,g,b))
        strip.show()
        time.sleep(FlashDelay/1000.0)

        setAll(strip, Color(0, 0, 0))
        strip.show()
        time.sleep(FlashDelay/1000.0)
    time.sleep(EndPause/1000)

#Threads for infinite chase
chase_stop = True
chase_speed = 50.0

def barChase(strip, color):
    """Chase bars"""
    global chase_speed
    # Bar 1
    allBarsOff(strip)
    if bar_4_sel.value == 1:
        for i in range(0, 15):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(float(chase_speed)/1000.0)
    allBarsOff(strip)

    # Bar 2
    if bar_3_sel.value == 1:
        for i in range(15, 30):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(float(chase_speed)/1000.0)
    allBarsOff(strip)
    
    # Bar 3
    if bar_2_sel.value == 1:
        for i in range(30, 45):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(float(chase_speed)/1000.0)
    allBarsOff(strip)
    
    # Bar 4
    if bar_1_sel.value == 1:
        for i in range(45, 60):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(float(chase_speed)/1000.0)
    allBarsOff(strip)
    
    # Bar 5
    if bar_5_sel.value == 1:
        for i in range(60, 101):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(float(chase_speed)/1000.0)
    allBarsOff(strip)
    
    # Bar 6
    if bar_6_sel.value == 1:
        for i in range(101, 144):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(float(chase_speed)/1000.0)
    allBarsOff(strip)
    
    # Bar 7
    if bar_7_sel.value == 1:
        for i in range(144, 185):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(float(chase_speed)/1000.0)
    allBarsOff(strip)
    
    # Bar 8
    if bar_8_sel.value == 1:
        for i in range(185, 227):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(float(chase_speed)/1000.0)
    allBarsOff(strip)

def chase_runner(strip):
    # Start chasing
    global r,g,b,chase_stop,chase_speed
    while True:
        if chase_stop == True:
            while True:
                time.sleep(150/1000.0)
                if chase_stop == False:
                    break
        barChase(strip, Color(r,g,b))

def stop_chasing():
    # Stop chasing
    global chase_stop
    chase_stop = True
    state_text.value = "OFF"

def start_chasing():
    # Stop chasing
    global chase_stop
    chase_stop = False
    state_text.value = "ON"

def update_chase_speed(slider_value):
    global chase_speed
    chase_speed = float(slider_value) * 10.0

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    # Start Led bars
    for i in range(strip.numPixels()):
        leds.append(False)

    print ("Started Led Console")
    chase_thread = threading.Thread(target=chase_runner, args=[strip])
    chase_thread.start()

    try:
        app = App(title="Led Console", width=1280, height=900)
        color_box = Box(app, layout="grid", width="fill", align="top", border=True)
        color_title = Text(color_box, grid=[0,0], text="Color", align="left", width="fill")
        color_radio = ButtonGroup(color_box, horizontal=True, grid=[0,1], options=["Red", "Blue", "Green", "White"], command=update_color)
        color_text = Text(color_box, grid=[2,1], size=14, align="left")
        fill_text1 = Text(color_box, grid=[1,1], text="       ")
        fill_text = Text(color_box, grid=[1,2], text="       ")

        bar_box = Box(app, layout="grid", width="fill", align="top", border=True)
        bar_title = Text(bar_box, grid=[0, 0], text="Bar Selection", align="left", width="fill")
        bar_1_sel = CheckBox(bar_box, grid=[1,1], text="Bar 1", command=update_bar_selection)
        bar_2_sel = CheckBox(bar_box, grid=[2,2], text="Bar 2", command=update_bar_selection)
        bar_3_sel = CheckBox(bar_box, grid=[1,3], text="Bar 3", command=update_bar_selection)
        bar_4_sel = CheckBox(bar_box, grid=[0,2], text="Bar 4", command=update_bar_selection)
        bar_5_sel = CheckBox(bar_box, grid=[5,1], text="Bar 5", command=update_bar_selection)
        bar_6_sel = CheckBox(bar_box, grid=[6,2], text="Bar 6", command=update_bar_selection)
        bar_7_sel = CheckBox(bar_box, grid=[5,3], text="Bar 7", command=update_bar_selection)
        bar_8_sel = CheckBox(bar_box, grid=[4,2], text="Bar 8", command=update_bar_selection)
        fill_text2 = Text(bar_box, grid=[0,4])
        fill_text20 = Text(bar_box, grid=[3,0], text="       ")

        basics_box = Box(app, layout="grid", width="fill", align="top", border=True)
        basics_title = Text(basics_box, grid=[0, 0], text="Basics", align="left", width="fill")
        on_all_btn = PushButton(basics_box, grid=[0, 1], command=lambda:allBarsOn(strip, Color(r, g, b)), text="All Bars On")
        on_selected_btn = PushButton(basics_box, grid=[1, 1], command=lambda:selectedBarsOn(strip, Color(r, g, b)), text="Selected Bars On")
        off_all_btn = PushButton(basics_box, grid=[2, 1], command=lambda:allBarsOff(strip), text="All Off")
        fill_text3 = Text(basics_box, grid=[0,2])

        flash_box = Box(app, layout="grid", width="fill", align="top", border=True)
        flash_title = Text(flash_box, grid=[0, 0], text="Flash Bars", align="left", width="fill")
        flash_1_bt = PushButton(flash_box, grid=[1,1], text="Flash Bar 1", command=lambda:flashBar1(strip, Color(r,g,b)))
        flash_2_bt = PushButton(flash_box, grid=[2,2], text="Flash Bar 2", command=lambda:flashBar2(strip, Color(r,g,b)))
        flash_3_bt = PushButton(flash_box, grid=[1,3], text="Flash Bar 3", command=lambda:flashBar3(strip, Color(r,g,b)))
        flash_4_bt = PushButton(flash_box, grid=[0,2], text="Flash Bar 4", command=lambda:flashBar4(strip, Color(r,g,b)))
        flash_5_bt = PushButton(flash_box, grid=[5,1], text="Flash Bar 5", command=lambda:flashBar5(strip, Color(r,g,b)))
        flash_6_bt = PushButton(flash_box, grid=[6,2], text="Flash Bar 6", command=lambda:flashBar6(strip, Color(r,g,b)))
        flash_7_bt = PushButton(flash_box, grid=[5,3], text="Flash Bar 7", command=lambda:flashBar7(strip, Color(r,g,b)))
        flash_8_bt = PushButton(flash_box, grid=[4,2], text="Flash Bar 8", command=lambda:flashBar8(strip, Color(r,g,b)))
        flash_all_bt = PushButton(flash_box, grid=[8,1], text="Flash All", command=lambda:flashAll(strip, Color(r,g,b)))
        flash_ssquare_bt = PushButton(flash_box, grid=[8,2], text="Flash Small", command=lambda:flashSmallSquare(strip, Color(r,g,b)))
        flash_bsquare_bt = PushButton(flash_box, grid=[8,3], text="Flash Big", command=lambda:flashBigSquare(strip, Color(r,g,b)))
        fill_text14 = Text(flash_box, grid=[3,1], text="       ")
        fill_text13 = Text(flash_box, grid=[7,1], text="       ")
        fill_text4 = Text(flash_box, grid=[0,4])
        
        chase_box = Box(app, layout="grid", width="fill", align="top", border=True)
        chase_title = Text(chase_box, grid=[0, 0], text="Chase", align="left", width="fill")
        bar_chase_on_bt = PushButton(chase_box, grid=[0, 1], command=start_chasing, text="Chase On")
        bar_chase_off_bt = PushButton(chase_box, grid=[1, 1], command=stop_chasing, text="Chase Off")
        text_chase = Text(chase_box, grid=[3,1], text="        Chase speed: ")
        speed_slider = Slider(chase_box, grid=[4, 1], command=update_chase_speed)
        state_text = Text(chase_box, grid=[5, 1])
        fill_text7 = Text(chase_box, grid=[0,2])

        strobe_box = Box(app, layout="grid", width="fill", align="top", border=True)
        strobe_title = Text(strobe_box, grid=[0, 0], text="Strobe", align="left", width="fill")
        strobe_btn = PushButton(strobe_box, grid=[0, 1], command=lambda:Strobe(strip), text="Strobe")
        repeat = Text(strobe_box, grid=[2,1], text="        Repeat: ")
        delay = Text(strobe_box, grid=[2,2], text="         Delay: ")
        endDelay = Text(strobe_box, grid=[2,3], text="     End Delay: ")
        repeat_slider = Slider(strobe_box, grid=[3, 1], command=update_strobe_count)
        delay_slider = Slider(strobe_box, grid=[3, 2], command=update_flash_delay)
        endDelay_slider = Slider(strobe_box, grid=[3, 3], command=update_endpause_count)
        fill_text9 = Text(strobe_box, grid=[0,4])
        
        effects_box = Box(app, layout="grid", width="fill", align="top", border=True)
        effects_title = Text(effects_box, grid=[0, 0], text="Other effects", align="left", width="fill")
        fade_in_btn = PushButton(effects_box, grid=[0, 1], command=lambda:FadeIn(strip), text="Fade In")
        fade_out_btn = PushButton(effects_box, grid=[1, 1], command=lambda:FadeOut(strip), text="Fade Out")
        running_btn = PushButton(effects_box, grid=[2, 1], command=lambda:RunningLights(strip), text="Running")
        full_swipe_btn = PushButton(effects_box, grid=[3, 1], command=lambda:colorWipe(strip, Color(r, g, b)), text="Wipe")
        theater_chase_btn = PushButton(effects_box, grid=[4, 1], command=lambda:theaterChase(strip, Color(r, g, b)), text="Theatre")
        fill_text5 = Text(effects_box, grid=[0,3])

        app.display()

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
