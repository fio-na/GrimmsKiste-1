#!/usr/bin/python3
import yaml
import subprocess
import textwrap
import RPi.GPIO as GPIO
import os
import time

time.sleep(2)

fp = open("/tmp/pid.yaml", mode="w", encoding="utf8")
yaml.dump(os.getpid(), fp, indent=1)

log = open("/home/pi/engine.log", mode="a", encoding="utf8", buffering=1)
log.write("Neustart\n")

stories = {}
a = open("/home/pi/GrimmsKiste-1/start.yaml", mode="r", encoding="utf8")
b = open("/home/pi/GrimmsKiste-1/Maus.yaml", mode="r", encoding="utf8")
c = open("/home/pi/GrimmsKiste-1/story.yaml", mode="r", encoding="utf8")

A1 = yaml.load(a)
B1 = yaml.load(b)
C1 = yaml.load(c)
stories.update(A1)
stories.update(B1)
stories.update(C1)
story = stories

curr=0

GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#fp = open("/tmp/pid.yaml", mode="w", encoding="utf8")
#yaml.dump(os.getpid(), fp, indent=1)

global start_time
start_time = time.time() - 3

def check_time_since_last_push_of_a_button():
    global start_time
    end_time = time.time()
    a = end_time - start_time
    start_time = end_time
    return a

def callback_1(channel):
    global curr
    print("gedrückt1", time.time())
    log.write("gedrückt 1\n")
    a = check_time_since_last_push_of_a_button()
    if a > 3:
        curr=1

def callback_2(channel):
    global curr
    print("gedrückt2", time.time())
    log.write("gedrückt 2\n")
    a = check_time_since_last_push_of_a_button()
    if a>3:
        curr=2
def callback_3(channel):
    global curr
    print("gedrückt3", time.time())
    log.write("gedrückt 3\n")
    state = GPIO.input(13)
    log.write("State: {}\n".format(state))
    if state==0: 
        a = check_time_since_last_push_of_a_button()
        if a>3:
            curr=3
    elif state==1 and curr==3:
        log.write("ACTION 3\n")

def callback_4(channel):
    global curr
    print("gedrückt4", time.time())
    log.write("gedrückt 4\n")
    a = check_time_since_last_push_of_a_button()
    if a>3:
        curr=4

GPIO.add_event_detect(5, GPIO.RISING, callback=callback_1, bouncetime=200)
GPIO.add_event_detect(6, GPIO.RISING, callback=callback_2, bouncetime=1000)
GPIO.add_event_detect(13, GPIO.BOTH, callback=callback_3, bouncetime=50)
GPIO.add_event_detect(19, GPIO.RISING, callback=callback_4, bouncetime=1000)

"""def send_to_printer2(text_to_print, type_of_printing):
    formatted_text = format_text(text_to_print)
    print(formatted_text)
    for i in formatted_text:
        
    if formatted_text[-1]
    if type_of_printing == "NoCutNoEmptyLines":
        formatted_text = format_text(text_to_print)
        print(formatted_text)
        for i in formatted_text:
            print(i)
            lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
            lpr.communicate(i.encode("utf-8"))
    if type_of_printing == "WithCut":
        lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
        lpr.communicate(text_to_print.encode("utf-8"))
    if type_of_printing == "WithEmptyLines":
        lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc", "-o", "PageType=1Fixed"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lpr.communicate("|".encode("utf-8"))"""

def send_to_printer_old(text_to_print):
    formatted_text = format_text(text_to_print)
    print(formatted_text)
    for i in formatted_text:
        print(i)
        lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
        lpr.communicate(i.encode("utf-8"))

def send_to_printer_with_cut(text_to_print):
    lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.communicate(text_to_print.encode("utf-8"))

def print_empty_lines():
    lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc", "-o", "PageType=1Fixed"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    lpr.communicate("|".encode("utf-8"))

def format_text(text_to_print):
    formatted_text = textwrap.wrap(text_to_print, 28)
    return formatted_text

def processState(state):
    if state == story["ende"]:
        send_to_printer_old(state["message"])
        send_to_printer_with_cut(80 * "-")
    else:
        send_to_printer_old(state["message"])
    if not "actions" in state:
        return None
    if "question" in state:
        send_to_printer_old(state["question"])
    else: send_to_printer_old(story["_default_question"])

    while True:
        action = requestAction(state["actions"])
        if action["next"] in story:
            return story[action["next"]]

def requestAction(actions):
    global curr
    for i, action in (enumerate(state["actions"], start=1)):
        if i == len(state["actions"]):
            send_to_printer_old("({}) {}".format(i, action["label"]))
            print_empty_lines()
        else:
            send_to_printer_old("({}) {}".format(i, action["label"]))
    while True:
        """global curr
        global last
        if curr == last and curr != 0:
            pass
        elif curr == 0:
            global last
        last = 0"""
        choice = curr - 1
        if 0 <= choice < len(actions):
            curr = 0
            if choice in actions:
                return actions[choice]
        time.sleep(0.01)
        '''elif choice > len(actions):
            global start_time
            print("ich wurde gedrückt")'''


send_to_printer_with_cut(28 * "-")
send_to_printer_old("Grimms Kiste".center(80, "-"))
last = 0

state = story["start"]
while state != None:
    state = processState(state)

