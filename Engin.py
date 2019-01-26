#!/usr/bin/python3
import yaml
import subprocess
import textwrap
import os
import time
from gpiozero import Button
import signal

with open("/tmp/pid.yaml", mode="w", encoding="utf8") as fp:
    yaml.dump(os.getpid(), fp, indent=1)

log = open("/home/pi/engine.log", mode="a", encoding="utf8", buffering=1)
log.write("Neustart\n")

story = {}

filelist = ["/home/pi/GrimmsKiste-1/start.yaml",
            "/home/pi/GrimmsKiste-1/Das-Baby-ist-verschwunden.yaml",
            "/home/pi/GrimmsKiste-1/Das-unerwartete-Feuer.yaml",
            "/home/pi/GrimmsKiste-1/Ein-erfolgreicher-Tag.yaml",
            "/home/pi/GrimmsKiste-1/Ein-Hund-namens-Bello.yaml",
            #"/home/pi/GrimmsKiste-1/Nur-mal-kurz-die-Welt-retten.yaml"
            ]

for file in filelist:
    with open(file, mode="r", encoding="utf8") as f:
        story_data = yaml.load(f)
        story.update(story_data)

curr=0

hold_time = 0.15

button1 = Button(5, hold_time)
button2 = Button(6, hold_time)
button3 = Button(13, hold_time)
button4 = Button(19, hold_time)

global start_time
start_time = time.time() - 2

def check_time_since_last_push_of_a_button():
    global start_time
    end_time = time.time()
    a = end_time - start_time
    start_time = end_time
    return a

def callback_1():
    global curr
    sec = time.time()
    log.write("{}, : gedrückt 1\n".format(sec))
    a = check_time_since_last_push_of_a_button()
    if a>2:
        curr=1

def callback_2():
    global curr
    sec = time.time()
    log.write("{}, : gedrückt 2\n".format(sec))
    a = check_time_since_last_push_of_a_button()
    if a>2:
        curr=2

def callback_3():
    global curr
    sec = time.time()
    log.write("{}, : gedrückt 3\n".format(sec))
    a = check_time_since_last_push_of_a_button()
    if a>2:
        curr=3

def callback_4():
    global curr
    sec = time.time()
    log.write("{}, : gedrückt 4\n".format(sec))
    a = check_time_since_last_push_of_a_button()
    if a>2:
        curr=4

button1.when_held = callback_1
button2.when_held = callback_2
button3.when_held = callback_3
button4.when_held = callback_4

def send_to_printer_old(text_to_print):
    formatted_text = "\n".join(format_text(text_to_print))
    lpr = subprocess.Popen(["/usr/bin/lp", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
    lpr.communicate(formatted_text.encode("utf-8"))

def send_list_to_printer(texts_to_print):
    texts_to_print.extend("." for _ in range(7))
    formatted_text = [format_text(i) for i in texts_to_print]
    joined_texts = ["\n".join(i) for i in formatted_text]
    final_texts = "\n".join(joined_texts)
    lpr = subprocess.Popen(["/usr/bin/lp", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
    lpr.communicate(final_texts.encode("utf-8"))

def send_to_printer_with_cut(text_to_print):
    lpr = subprocess.Popen("/usr/bin/lp", stdin=subprocess.PIPE)
    lpr.communicate(text_to_print.encode("utf-8"))

def format_text(text_to_print):
    return textwrap.wrap(text_to_print, 28)

def processState(state):
    if state == story["ende"]:
        send_to_printer_old(state["message"])
        for_printing = [state["message"]]
        send_to_printer_with_cut(28 * "-")
    else:
        send_to_printer_old(state["message"])
    if not "actions" in state:
        return None
    if "question" in state:
        send_to_printer_old(state["question"])
    else:
        send_to_printer_old(story["_default_question"])
    action = requestAction(state["actions"])
    return story[action["next"]]

def requestAction(actions):
    global curr
    options_list = ["({}) {}".format(i, action["label"]) for i, action in enumerate(state["actions"], start=1)]
    send_list_to_printer(options_list)
    while True:
        try:
            choice = curr - 1
            if 0 <= choice < len(actions):
                curr = 0
                return actions[choice]
        except:
            time.sleep(0.01)
            pass


def print_header():


def


send_to_printer_with_cut(28 * "-")
send_to_printer_old("Grimms Kiste".center(84, "-"))
last = 0

state = story["start"]
while state != None:
    state = processState(state)
