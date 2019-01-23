#!/usr/bin/python
# Simple script for shutting down the raspberry Pi at the press of a button.
# by Inderpreet Singh
import RPi.GPIO as GPIO
from gpiozero import Button
import time
import os
import signal
# Use the Broadcom SOC Pin numbers
# Setup the Pin with Internal pullups enabled and PIN in reading mode.
"""GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)"""
shutdown_button = Button(17, hold_time=3)
restart_button = Button(27, hold_time=3)
# Our function on what to do when the button is pressed
def shutdown(channel):
      print ("shutdown pressed")
      os.system("sudo shutdown -h now")
def restart(channel):
      print ("restart pressed")
      os.system("sudo pkill -F /tmp/pid.yaml")
# Add our function to execute when the button pressed event happens
"""GPIO.add_event_detect(17, GPIO.FALLING, callback = shutdown, bouncetime = 2000)
GPIO.add_event_detect(27, GPIO.FALLING, callback = restart, bouncetime = 2000)"""
shutdown_button.when_held = shutdown
restart_button.when_held = restart
# Now wait!
#while 1:
      #time.sleep(1)
signal.pause()
