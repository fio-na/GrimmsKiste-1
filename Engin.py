import yaml
import subprocess
import locale

fh = open("story.yaml", mode="r", encoding="utf-8")
story = yaml.load(fh)

lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)

def print_to_printer(text_to_print):
    #lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.stdin.write(text_to_print.encode("utf-8"))

def processState(state):
    print_to_printer("hi")
    print_to_printer("hallo")
    print_to_printer(state["message"])

    if not "actions" in state:
        return None
    if "question" in state:
        print_to_printer(state["question"])
    else: print_to_printer(story["_default_question"])

    action = requestAction(state["actions"])
    return story[action["next"]]

def requestAction(actions):
    print_to_printer("\n")
    for i, action in (enumerate(state["actions"], start=1)):
        print_to_printer("({}) {}".format(i, action["label"]))

    while True:
        try:
            choice = int(input(story["_prompt"])) - 1
            if 0 <= choice < len(actions):
                return actions[choice]

        except:
            pass


print_to_printer("Grimms Kiste".center(80, "-"))

state = story["start"]
while state != None:
    state = processState(state)

print_to_printer(80 * "-")
