#!/usr/bin/python3

import RPi.GPIO as GPIO
import subprocess
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
buttonstatus = 0

def callback_restart(self):
    print("Knopf gedrückt")
    global buttonstatus
    buttonstatus = 1

def cut_paper():
    lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.communicate(80 * "-".encode("utf-8"))

def restart_engine():
    print("Neustart")
    os.execl("~/GrimmsKiste-1/Engin.py")

print("Buttonscript running")
GPIO.add_event_detect(6, GPIO.RISING, callback=callback_restart, bouncetime=500)

while True:
    if buttonstatus == 0:
        pass
    elif buttonstatus == 1:
        cut_paper()
        restart_engine()
        buttonstatus = 0
