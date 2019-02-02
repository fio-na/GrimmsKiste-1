#!/usr/bin/python3
import yaml
import subprocess
import textwrap
import os
import time
from gpiozero import Button

#writes the pid of a process into a file, which is used by a different script to kill the process, used for restarting
with open("/tmp/pid.yaml", mode="w", encoding="utf8") as fp:
    yaml.dump(os.getpid(), fp, indent=1)

#read this log to control if the program has restarted or a button has been pushed
log = open("/home/pi/engine.log", mode="a", encoding="utf8", buffering=1)
log.write("restart\n")

story = {}

#here you can add new stories, just add add a comma and the path to the story
filelist = ["/home/pi/GrimmsKiste-1/start.yaml",
            "/home/pi/GrimmsKiste-1/Das-Baby-ist-verschwunden.yaml",
            "/home/pi/GrimmsKiste-1/Das-unerwartete-Feuer.yaml",
            "/home/pi/GrimmsKiste-1/Ein-erfolgreicher-Tag.yaml",
            "/home/pi/GrimmsKiste-1/Ein-Hund-namens-Bello.yaml",
            "/home/pi/GrimmsKiste-1/Nur-mal-kurz-die-Welt-retten.yaml"
            ]

#this pulls the data of the story files into one data structure - story
for file in filelist:
    with open(file, mode="r", encoding="utf8") as f:
        story_data = yaml.load(f)
        story.update(story_data)

#here you can specify the amount of time in seconds a button needs to be pushed, implemented because our buttons got detected to easily
hold_time = 0.1

#specify the pins (BCM) you use for your buttons
button1 = Button(5, hold_time=hold_time)
button2 = Button(6, hold_time=hold_time)
button3 = Button(13, hold_time=hold_time)
button4 = Button(19, hold_time=hold_time)

global start_time
start_time = time.time() - 1.7

#buttons pushed less then a specified amount of time since the last push will be ignored, because the printer is slower than the program, specify the time in the callbacks
def check_time_since_last_push_of_a_button():
    global start_time
    push_time = time.time()
    secs_since_last_push = push_time - start_time
    start_time = push_time
    return secs_since_last_push

#these specify what should happen when a button is pushed, writes it to the log, checks time since last pushed button and if it is greater than specified time changes the state and prints the next part of the story
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

#specifies which callbacks shall be used for which button
button1.when_held = callback_1
button2.when_held = callback_2
button3.when_held = callback_3
button4.when_held = callback_4

#uses lp to send data to printer, we included options specified for pur printer
def send_string_to_printer(text_to_print):
    formatted_text = "\n".join(format_text(text_to_print))
    lpr = subprocess.Popen(["/usr/bin/lp", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
    lpr.communicate(formatted_text.encode("utf-8"))

#formats all the elements in a list, joins them to one string and prints that string
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

#formats strings into a list where each element is no longer than 28 characters, doesn't break words, adjust 28 to fit your page size
def format_text(text_to_print):
    return textwrap.wrap(text_to_print, 28)

#sends a cut to the printer in case the last story wasn't completed, then prints header
def print_header():
    send_to_printer_with_cut(28 * "-")
    send_string_to_printer("Grimms Kiste".center(84, "-"))

#collects elements which need to be printed into a list
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
        #if no actions are in the state, the game is over, therefore the question needs to be deleted and a message that the story is over is appended to the list
        del list_for_printing[-1]
        list_for_printing.append("Damit ist die Geschichte zu Ende.")
    send_list_to_printer(list_for_printing)

#called by the push of a button, collects the information about the next state of the story from the data structure and prints the next state
def process_state(chosen_action, button):
    global state
    action = chosen_action[button]
    state = story[action["next"]]
    print_current_state(state)

#sets the first state to start, which is the list of stories to choose from
state = story["start"]

#the actual execution part
print_header()
print_current_state(state)
while "actions" in state:
    #waiting for buttons being pushed
    time.sleep(0.5)
send_to_printer_with_cut(28 * "-")
#giving the reader some time to read the last part before restarting
time.sleep(3.5)
