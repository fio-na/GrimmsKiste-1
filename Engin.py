import yaml
import subprocess
import locale

fh = open("story.yaml", mode="r", encoding="utf-8")
story = yaml.load(fh)

lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)

def print_to_printer(text_to_print):
    #lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.stdin.write(text_to_print.encode("utf-8"))
    #if lpr.communicate is used, it prints directly when it is called. however you cannot keep the pipe open, and uf you open and close it, the pater gets cut
    #if lpr.stdin.write is used, it prints only when the program is finished, but if you open lpr in the beginning of the process you can print multiple things without the paper being cut

def processState(state):
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
