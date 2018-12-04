import yaml
import subprocess
import textwrap
import RPi.GPIO as GPIO
import time
#pyphen

fh = open("story.yaml", mode="r", encoding="utf-8")
story = yaml.load(fh)

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def callback_restart():
    restart_engine()

GPIO.add_event_detect(5, GPIO.RISING, callback=callback_restart, bouncetime=500)

def send_to_printer(text_to_print):
    formatted_text = format_text(text_to_print)
    for i in formatted_text:
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
    for i in range(7):
        lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
        lpr.communicate("a".encode("utf-8"))

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
    while True:
        eingabe = input(story["_prompt"])
        if eingabe == "Ende" or eingabe == "ende":
            raise SystemExit("Ende")
        else:
            try:
                choice = int(eingabe) - 1
                if 0 <= choice < len(actions):
                    return actions[choice]
            except:
                pass

def restart_engine():
    #send_to_printer_with_cut(80 * "-")
    send_to_printer("Grimms Kiste".center(80, "-"))
    global state
    state = story["start"]
    while state != None:
        state = processState(state)

send_to_printer("Grimms Kiste".center(80, "-"))

state = story["start"]
while state != None:
    state = processState(state)

