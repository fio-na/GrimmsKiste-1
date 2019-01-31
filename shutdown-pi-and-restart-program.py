#!/usr/bin/python
from gpiozero import Button
import os
import signal

#specifying the pins used and the time the buttons need to be pushed before executing
shutdown_button = Button(17, hold_time=3)
restart_button = Button(27, hold_time=3)

#callbacks specifying what should happen when a button is pushed, restart kills the engine, while a systemd process checks every two seconds if it is running and restarts it if necessary
def shutdown(channel):
      print ("shutdown pressed")
      os.system("sudo shutdown -h now")
def restart(channel):
      print ("restart pressed")
      os.system("sudo pkill -F /tmp/pid.yaml")

shutdown_button.when_held = shutdown
restart_button.when_held = restart

#waiting for input
signal.pause()
