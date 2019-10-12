import argparse
from random import randint
import os.path
parser = argparse.ArgumentParser()
parser.add_argument('-input')
args = parser.parse_args()
print(args)

class Match:
    def __init__(self, b1, b2, g1, g2):
        self.b1 = b1
        self.b2 = b2
        self.g1 = g1
        self.g2 = g2

class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.lastMatch = -6

schools = []
totalRounds = int(args.n)

def process(line):
    values = line.rstrip().split(",")
    schools.append(Team(values[0], values[1]))

with open(args.input) as f:
    for line in f:
        process(line)

matches = []
for i in range(totalRounds):
    teamsLeft = schools.copy()
    matchedTeams = []
    alreadyPlayed = []
    while len(teamsLeft) >= 4:
        for i in range(4):
            team = randint(0, len(teamsLeft) - 1)
            while teamsLeft[team].lastMatch == len(matches) - 1:
                team = randint(0, len(teamsLeft) - 1)
            matchedTeams.append(teamsLeft[team])
            alreadyPlayed.append(teamsLeft[team])
            del teamsLeft[team]
        matches.append(Match(matchedTeams[0], matchedTeams[1], matchedTeams[2], matchedTeams[3]))
        for team in matchedTeams:
            team.lastMatch = len(matches) - 1
        matchedTeams = []
    if len(teamsLeft) != 0:
        matchedTeams.extend(teamsLeft)
        for i in range(4 - len(teamsLeft)):
            team = randint(0, len(alreadyPlayed) - 1)
            while alreadyPlayed[team].lastMatch == len(matches) - 1:
                team = randint(0, len(alreadyPlayed) - 1)
            matchedTeams.append(alreadyPlayed[team])
            del alreadyPlayed[team]
        matches.append(Match(matchedTeams[0], matchedTeams[1], matchedTeams[2], matchedTeams[3]))
        for team in matchedTeams:
            team.lastMatch = len(matches) - 1
        matchedTeams = []

writeHeader = False
if not os.path.isfile("matches.csv"):
    writeHeader = True

with open("matches.csv", "a") as f:
    if writeHeader:
        f.write("Blue 1 ID, Blue 1 Name, Blue 2 ID, Blue 2 Name, Gold 1 ID, Gold 1 Name, Gold 2 ID, Gold 2 Name\n")
    for m in matches:
        f.write(m.b1.id + "," + m.b1.name +
        "," + m.b2.id + "," + m.b2.name +
        "," + m.g1.id + "," + m.g1.name +
        "," + m.g2.id + "," +
        m.g2.name + "\n")
