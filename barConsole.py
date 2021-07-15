#!/usr/bin/env python3.7
# Based on:
#   rpi_ws281x library
#   Author: Tony DiCola (tony@tonydicola.com)
# 
# Additional work by:
#   Joao Ferreira (W.Labs)
 
import time
import math
import guizero
from rpi_ws281x import *
from guizero import App, Text, PushButton, Box, CheckBox, Combo, ButtonGroup, Slider
import argparse
import threading
#import multiprocessing 

# LED strip configuration:
LED_COUNT      = 150     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Global color variables
r = 0
g = 0
b = 0

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms/1000.0)

# Update the red value
def updateRed(slider_value):
    global r
    r = (int(slider_value)/100) * 255

# Update green value
def updateGreen(slider_value):
    global g
    g = (int(slider_value)/100) * 255

# Update blue value
def updateBlue(slider_value):
    global b
    b = (int(slider_value)/100) * 255

# Fade up.. most left bar
def updateMostLeft(slider_value, strip):
    global r, g, b
    for x in range(0, 30):
        red = int(math.floor((slider_value / 100.0) * r))
        green = int(math.floor((slider_value / 100.0) * g))
        blue = int(math.floor((slider_value / 100.0) * b))
        strip.setPixelColor(x, Color(red, green, blue))
    strip.show()

# Fade up.. left bar
def updateLeft(slider_value, strip):
    global r, g, b
    for x in range(30, 60):
        red = int(math.floor((slider_value / 100.0) * r))
        green = int(math.floor((slider_value / 100.0) * g))
        blue = int(math.floor((slider_value / 100.0) * b))
        strip.setPixelColor(x, Color(red, green, blue))
    strip.show()

# Fade up.. center bar
def updateCenter(slider_value, strip):
    global r, g, b
    for x in range(60, 90):
        red = int(math.floor((slider_value / 100.0) * r))
        green = int(math.floor((slider_value / 100.0) * g))
        blue = int(math.floor((slider_value / 100.0) * b))
        strip.setPixelColor(x, Color(red, green, blue))
    strip.show()

# Fade up.. right bar
def updateRight(slider_value, strip):
    global r, g, b
    for x in range(90, 120):
        red = int(math.floor((slider_value / 100.0) * r))
        green = int(math.floor((slider_value / 100.0) * g))
        blue = int(math.floor((slider_value / 100.0) * b))
        strip.setPixelColor(x, Color(red, green, blue))
    strip.show()

# Fade up.. most right bar
def updateMostRight(slider_value, strip):
    global r, g, b
    for x in range(120, 150):
        red = int(math.floor((slider_value / 100.0) * r))
        green = int(math.floor((slider_value / 100.0) * g))
        blue = int(math.floor((slider_value / 100.0) * b))
        strip.setPixelColor(x, Color(red, green, blue))
    strip.show()

# Fade up.. all bars
def updateMaster(slider_value, strip):
    global r, g, b
    for x in range(0, 150):
        red = int(math.floor((slider_value / 100.0) * r))
        green = int(math.floor((slider_value / 100.0) * g))
        blue = int(math.floor((slider_value / 100.0) * b))
        strip.setPixelColor(x, Color(red, green, blue))
    strip.show()

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

    print ("Started Led Bar Console")
    
    # Start dimming thread
    # chase_thread = threading.Thread(target=chase_runner, args=[strip])
    # chase_thread.start()

    try:
        app = App(title="Led Bar Console", width=1280, height=900)
        dimming_box = Box(app, layout="grid", width="fill", align="top", border=True)
        dimming_title = Text(dimming_box, grid=[0,0], text="Dimmmer", align="left", width="fill")
        
        mlft_slider = Slider(dimming_box, grid=[2,2], align="left", horizontal=False, command=lambda:updateMostLeft(mlft_slider.value, strip))
        ml_text = Text(dimming_box, grid=[2,3], text="  MLeft", align="left", width="fill")
        
        lft_slider = Slider(dimming_box, grid=[4,2], align="left", horizontal=False, command=lambda:updateLeft(lft_slider.value, strip))
        l_text = Text(dimming_box, grid=[4,3], text="    Left", align="left", width="fill")
        
        ctr_slider = Slider(dimming_box, grid=[6,2], align="bottom", horizontal=False, command=lambda:updateCenter(ctr_slider.value, strip))
        c_text = Text(dimming_box, grid=[6,3], text="  Center", align="bottom", width="fill")
        
        rgt_slider = Slider(dimming_box, grid=[8,2], align="right", horizontal=False, command=lambda:updateRight(rgt_slider, strip))
        r_text = Text(dimming_box, grid=[8,3], text="Right", align="right", width="fill")
        
        mrgt_slider = Slider(dimming_box, grid=[10,2], align="right", horizontal=False, command=lambda:updateMostRight(mrgt_slider.value, strip))
        mr_text = Text(dimming_box, grid=[10,3], text="  MRight", align="right", width="fill")

        master_slider = Slider(dimming_box, grid=[16,2], align="right", horizontal=False, command=lambda:updateMaster(master_slider.value, strip))
        mr_text = Text(dimming_box, grid=[16,3], text="   Master", align="right", width="fill")

        
        color_box = Box(app, layout="grid", width="fill", align="top", border=True)
        color_title = Text(color_box, grid=[0,0], text="Color", align="left", width="fill")
        
        red_slider = Slider(color_box, grid=[2,2], horizontal=False, command=updateRed)
        r_text = Text(color_box, grid=[2,3], text="Red", align="left", width="fill")
        
        green_slider = Slider(color_box, grid=[3,2], horizontal=False, command=updateGreen)
        g_text = Text(color_box, grid=[3,3], text="Green", align="left", width="fill")

        blue_slider = Slider(color_box, grid=[4,2], horizontal=False, command=updateBlue)
        b_text = Text(color_box, grid=[4,3], text="Blue", align="right", width="fill")

        quick_box = Box(app, layout="grid", width="fill", align="top", border=True)
        quick_title = Text(quick_box, grid=[0,0], text="Quick Commands", align="left", width="fill")
        on_bt = PushButton(quick_box, grid=[0,2], text="ON ", command=lambda:colorWipe(strip, Color(int(r), int(g), int(b)), 10))
        off_bt = PushButton(quick_box, grid=[1,2], text="OFF", command=lambda:colorWipe(strip, Color(0,0,0), 0))

        app.display()

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
