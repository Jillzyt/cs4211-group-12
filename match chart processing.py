from collections import defaultdict, Counter
import re, sys

path = r'C:\\Users\\priso\\OneDrive - National University of Singapore\\Y4S1\\CS4211\\Project\\'
filename = r'match_chart.txt'

hm = {
    'ml': defaultdict(lambda: defaultdict(lambda: Counter())),
    'fz': defaultdict(lambda: defaultdict(lambda: Counter())),
}
ml_rally_action_count = 0
fz_rally_action_count = 0

ml_serve_action_count = 0
fz_serve_action_count = 0

with open(f"{path}{filename}", encoding='utf8') as f:
    lines = f.readlines()
    for line in lines:
        if len(line.strip()) == 0:
            continue
        replacedString = re.sub("[,:'‘’.]", " ", line)
        replacedString = re.sub(' +', ' ', replacedString)
        if 'forehand' not in replacedString and 'backhand' not in replacedString:
            continue
        splitString = replacedString.split()
        playerName = splitString[0].lower()
        if playerName[0] == "m":
            playerName = "ml"
            if splitString[3] == "2" or splitString[3] == "1":
                print(line)
        else:
            if splitString[3] == "3" or splitString[3] == "4":
                print(line)
            playerName = 'fz'
        gameAction = splitString[1].lower()
        if "defence" in gameAction:
            gameAction.replace("defence", "defense")
        if "serve" not in gameAction:
            if playerName == "ml":
                ml_rally_action_count += 1
            else:
                fz_rally_action_count += 1
        elif "serve" in gameAction:
            if playerName == "ml":
                ml_serve_action_count += 1
            else:
                fz_serve_action_count += 1
        strokePosition = splitString[2].lower()
        ballPosition = splitString[3]
        if "fail" in gameAction:
            ballPosition = "5"
        hm[playerName][gameAction][strokePosition][ballPosition] += 1

with open(f'{path}result.txt', 'w', encoding='utf8') as f:
    stringToWrite = ""
    for player, actions in hm.items():
        stringToWrite += player + ": \n"
        for action, positions in actions.items():
            if "serve" not in action:
                if player == "ml":
                    actionCount = ml_rally_action_count
                else:
                    actionCount = fz_rally_action_count
            else:
                if player == "ml":
                    actionCount = ml_serve_action_count
                else:
                    actionCount = fz_serve_action_count
            stringToWrite += " " * 4
            stringToWrite += action + ": \n"
            for position, ballPositions in positions.items():
                stringToWrite += " " * 8
                stringToWrite += position + ": \n"
                for ballPosition, count in ballPositions.items():
                    stringToWrite += " " * 12
                    stringToWrite += ballPosition + ": " + str(count) + ", " + str(count/actionCount) + "\n"

        stringToWrite += "\n"
    stringToWrite += "Total: " + str(ml_rally_action_count + fz_rally_action_count + ml_serve_action_count + fz_serve_action_count) + "\n"
    f.write(stringToWrite)
    f.close()

        