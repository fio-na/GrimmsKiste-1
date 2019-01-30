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
log.write("restart\n")

story = {}

filelist = ["/home/pi/GrimmsKiste-1/start.yaml",
            "/home/pi/GrimmsKiste-1/Das-Baby-ist-verschwunden.yaml",
            "/home/pi/GrimmsKiste-1/Das-unerwartete-Feuer.yaml",
            "/home/pi/GrimmsKiste-1/Ein-erfolgreicher-Tag.yaml",
            "/home/pi/GrimmsKiste-1/Ein-Hund-namens-Bello.yaml",
            "/home/pi/GrimmsKiste-1/Nur-mal-kurz-die-Welt-retten.yaml"
            ]

for file in filelist:
    with open(file, mode="r", encoding="utf8") as f:
        story_data = yaml.load(f)
        story.update(story_data)

hold_time = 0.2

button1 = Button(5, hold_time=hold_time)
button2 = Button(6, hold_time=hold_time)
button3 = Button(13, hold_time=hold_time)
button4 = Button(19, hold_time=hold_time)

global start_time
start_time = time.time() - 1.7

def check_time_since_last_push_of_a_button():
    global start_time
    push_time = time.time()
    secs_since_last_push = push_time - start_time
    start_time = push_time
    return secs_since_last_push

def callback_1():
    sec = time.time()
    log.write("{}, : pushed 1\n".format(sec))
    a = check_time_since_last_push_of_a_button()
    if a>1.7:
        current_action = state["actions"]
        if len(current_action) >= 1:
            process_state(current_action, 0)
        else:
            pass

def callback_2():
    sec = time.time()
    log.write("{}, : pushed 2\n".format(sec))
    a = check_time_since_last_push_of_a_button()
    if a>1.7:
        current_action = state["actions"]
        if len(current_action) >= 2:
            process_state(current_action, 1)
        else:
            pass

def callback_3():
    sec = time.time()
    log.write("{}, : pushed 3\n".format(sec))
    a = check_time_since_last_push_of_a_button()
    if a>1.7:
        current_action = state["actions"]
        if len(current_action) >= 3:
            process_state(current_action, 2)
        else:
            pass

def callback_4():
    sec = time.time()
    log.write("{}, : pushed 4\n".format(sec))
    a = check_time_since_last_push_of_a_button()
    if a>1.7:
        current_action = state["actions"]
        if len(current_action) >= 4:
            process_state(current_action, 3)
        else:
            pass

button1.when_held = callback_1
button2.when_held = callback_2
button3.when_held = callback_3
button4.when_held = callback_4

def send_string_to_printer(text_to_print):
    formatted_text = "\n".join(format_text(text_to_print))
    lpr = subprocess.Popen(["/usr/bin/lp", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
    lpr.communicate(formatted_text.encode("utf-8"))

def send_list_to_printer(texts_to_print):
    texts_to_print.extend("." for _ in range(8))
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

def print_header():
    send_to_printer_with_cut(28 * "-")
    send_string_to_printer("Grimms Kiste".center(84, "-"))

def print_current_state(current_state):
    list_for_printing = []
    list_for_printing.append(current_state["message"])
    if "question" in state:
        list_for_printing.append(current_state["question"])
    else:
        list_for_printing.append(story["_default_question"])
    if "actions" in state:
        list_for_printing.extend(["({}) {}".format(i, action["label"]) for i, action in enumerate(current_state["actions"], start=1)])
    else:
        del list_for_printing[-1]
        list_for_printing.append("Damit ist die Geschichte zu Ende.")
    send_list_to_printer(list_for_printing)

def process_state(chosen_action, button):
    global state
    action = chosen_action[button]
    state = story[action["next"]]
    print_current_state(state)

state = story["start"]

print_header()
print_current_state(state)
while "actions" in state:
    time.sleep(0.5)
send_to_printer_with_cut(28 * "-")
time.sleep(3.5)
