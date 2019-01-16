#!/usr/bin/python3
import yaml
import subprocess
import textwrap
import RPi.GPIO as GPIO
import os

fp = open("/tmp/pid.yaml", mode="w", encoding="utf8")
yaml.dump(os.getpid(), fp, indent=1)

geschichten = {}
a = open("start.yaml", mode="r", encoding="utf8")
b = open("Maus.yaml", mode="r", encoding="utf8")
c = open("story.yaml", mode="r", encoding="utf8")

A1 = yaml.load(a)
B1 = yaml.load(b)
C1 = yaml.load(c)
geschichten.update(A1)
geschichten.update(B1)
geschichten.update(C1)
story = geschichten

curr=0

GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
        lpr.communicate(i.encode("utf-8"))

def send_to_printer_with_cut(text_to_print):
    lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.communicate(text_to_print.encode("utf-8"))

def format_text(text_to_print):
    formatted_text = textwrap.wrap(text_to_print, 28)
    return formatted_text

def print_empty_lines():
    lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc", "-o", "PageType=1Fixed"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    lpr.communicate("|".encode("utf-8"))

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
    for i, action in (enumerate(state["actions"], start=1)):
        if i == len(state["actions"]):
            send_to_printer("({}) {}".format(i, action["label"]))
            print_empty_lines()
        else:
            send_to_printer("({}) {}".format(i, action["label"]))
    while True:
        """global curr
        global last
        if curr == last and curr != 0:
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


send_to_printer_with_cut(28 * "-")
send_to_printer("Grimms Kiste".center(80, "-"))
last = 0

state = story["start"]
while state != None:
    state = processState(state)

