from Story import story

def processState(state):
    print()
    print(state["message"])

    if not "actions" in state:
        return None

    if "question" in state: print(state["question"])
    else: print(story["_default_question"])

    action = requestAction(state["actions"])
    return story[action["next"]]

def requestAction(actions):
    print()
    for i, action in (enumerate(state["actions"], start=1)):
        print("({}) {}".format(i, action["label"]))
    print()

    while True:
        try:
            choice = int(input(story["_prompt"])) - 1
            if 0 <= choice < len(actions):
                return actions[choice]

        except:
            pass

print("Grimms Kiste".center(80, "-"))

state = story["start"]
while state != None:
    state = processState(state)

print(80 * "-")
