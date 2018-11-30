import yaml
import subprocess

fh = open("story.yaml", mode="r", encoding="utf-8")
story = yaml.load(fh)

def send_to_printer(text_to_print):
    #formatted_text = format_text_for_printing(text_to_print.encode("utf-8"))
    lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
    lpr.communicate(text_to_print.encode("utf-8"))

def send_to_printer_with_cut(text_to_print):
    #formatted_text = format_text_for_printing(text_to_print.encode("utf-8"))
    lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.communicate(text_to_print.encode("utf-8"))

def format_text_for_printing(text_to_print):
    formatting = subprocess.Popen(["/usr/bin/fold", "-s", "-w", "29"])
    return formatting.communicate(text_to_print)

def print_empty_lines():
    for i in range(3):
        lpr = subprocess.Popen(["/usr/bin/lpr", "-o", "PageCutType=0NoCutPage", "-o", "DocCutType=0NoCutDoc"], stdin=subprocess.PIPE)
        lpr.communicate("\n".encode("utf-8"))

def processState(state):
    if state == story["ende"]:
        send_to_printer(state["message"])
        send_to_printer_with_cut(80 * "-")
    else:
        send_to_printer(state["message"])
        print_empty_lines()
    if not "actions" in state:
        return None
    if "question" in state:
        send_to_printer(state["question"])
        print_empty_lines()
    else: send_to_printer(story["_default_question"])

    action = requestAction(state["actions"])
    print_empty_lines()
    return story[action["next"]]

def requestAction(actions):
    send_to_printer("\n")
    for i, action in (enumerate(state["actions"], start=1)):
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
