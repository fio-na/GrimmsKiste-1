import yaml
import subprocess
import textwrap
#pyphen

fh = open("story.yaml", mode="r", encoding="utf-8")
story = yaml.load(fh)

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
        try:
            choice = int(input(story["_prompt"])) - 1
            if 0 <= choice < len(actions):
                return actions[choice]

        except:
            pass


send_to_printer("Grimms Kiste".center(80, "-"))

state = story["start"]
while state != None:
    state = processState(state)
