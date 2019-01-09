#!/usr/bin/python3
import yaml
import subprocess
import textwrap
import os
import RPi.GPIO as GPIO
import time
#pyphen

fh = open("/home/pi/GrimmsKiste-1/story.yaml", mode="r", encoding="utf-8")
story = yaml.load(fh)

GPIO.setmode(GPIO.BCM)

# this enables us to demonstrate both rising and falling edge detection
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
curr=0

def callback_1(channel):
    global curr
    curr=1
def callback_2(channel):
    global curr
    curr=2
def callback_3(channel):
    global curr
    curr=3
def callback_4(channel):
    global curr
    curr=4

GPIO.add_event_detect(5, GPIO.RISING, callback=callback_1, bouncetime=500)
GPIO.add_event_detect(6, GPIO.RISING, callback=callback_2, bouncetime=500)
GPIO.add_event_detect(13, GPIO.RISING, callback=callback_3, bouncetime=500)
GPIO.add_event_detect(19, GPIO.RISING, callback=callback_4, bouncetime=500)

def send_to_printer(text_to_print):
    formatted_text = format_text(text_to_print)
    print(formatted_text)
    for i in formatted_text:
        print(i)
        #print(i.encode("utf-8"))
        lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
        lpr.communicate(i.encode("utf-8"))

"""def send_to_printer_with_cut(text_to_print):
    formatted_text = format_text(text_to_print)
    for i in formatted_text:
        lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
        lpr.communicate(i.encode("utf-8"))"""

def send_to_printer_with_cut(text_to_print):
    lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.communicate(text_to_print.encode("utf-8"))

def format_text(text_to_print):
    formatted_text = textwrap.wrap(text_to_print, 28)
    return formatted_text

def print_empty_lines():
    #send_to_printer("strhtzhjh esrhreajh jzujtuik8zi8lkoloil 435qzuqz4tw5zr6hzjukti z89p8zpot7irt6ue5z4 q3t43aaaaaaaaaaaaaaaae65uuuuu 6r7iii87o89oi465tf43rf q34t45z5tz64w5z")
    lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc", "-o", "PageType=1Fixed"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = lpr.communicate("Test".encode("utf-8"))
    print(result)

def processState(state):
    if state == story["ende"]:
        send_to_printer(state["message"])
        send_to_printer_with_cut(80 * "-")
    else:
        send_to_printer(state["message"])
    if not "actions" in state:
        return None
    if "question" in state:
        send_to_printer(state["question"])
    else: send_to_printer(story["_default_question"])

    action = requestAction(state["actions"])
    return story[action["next"]]

def requestAction(actions):
    #send_to_printer("\n")
    for i, action in (enumerate(state["actions"], start=1)):
        if i == len(state["actions"]):
            send_to_printer("({}) {}".format(i, action["label"]))
            print_empty_lines()
        else:
            send_to_printer("({}) {}".format(i, action["label"]))
    """while True:
        eingabe = input(story["_prompt"])
        if eingabe == "Ende" or eingabe == "ende":
            raise SystemExit("Ende")
        else:
            try:
                choice = int(eingabe) - 1
                if 0 <= choice < len(actions):
                    return actions[choice]
            except:
                pass"""
    while True:
        #global curr
        #global last
        """if curr == last and curr != 0:
            pass
        elif curr == 0:
            global last
            last = 0"""
        if True:
            try:
                choice = curr - 1
                if 0 <= choice < len(actions):
                    global curr
                    curr = 0
                    return actions[choice]
            except:
                pass


#os.system("~/GrimmsKiste-1/restart-button.py")

send_to_printer("Grimms Kiste".center(80, "-"))
last = 0

state = story["start"]
while state != None:
    state = processState(state)

#state = story["start"]
