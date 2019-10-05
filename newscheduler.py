import sys
from random import randint
import os.path
from itertools import permutations

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
        self.canPlay = 0
        self.playedWith = []

schools = []

def process(line):
    values = line.rstrip().split(",")
    schools.append(Team(values[0], values[1]))

input = sys.stdin.readline().rstrip().split(" ")
csvFile = input[0]
roundsPerTeam = int(input[1])

with open(csvFile) as f:
    for line in f:
        process(line)
gap = 2 #Time before school can play again
matches = []
teamsLeft = schools.copy()
totalRounds = len(schools)//4*3
for i in range(totalRounds):
    matchedTeams = []
    if len(teamsLeft) >= 4:
        j = 0
        while j < 4:
            team = teamsLeft[randint(0, len(teamsLeft) - 1)]
            if team.canPlay >= 0:
                matchedTeams.append(team)
                teamsLeft.remove(team)
                j += 1
    else:
        matchedTeams = teamsLeft[:]
        restOfTeams = 4 - len(matchedTeams)
        teamsLeft = schools.copy()
        k = 0
        while k < restOfTeams:
            team = teamsLeft[randint(0, len(teamsLeft)-1)]
            if team.canPlay >= 0 and team not in matchedTeams:
                matchedTeams.append(team)
                teamsLeft.remove(team)
                k += 1
        perm = list(permutations(range(4)))
        for p in perm:
            if matchedTeams[p[0]] not in matchedTeams[p[1]].playedWith and matchedTeams[p[2]] not in matchedTeams[p[3]].playedWith:
                matches.append(Match(matchedTeams[p[0]],matchedTeams[p[1]],matchedTeams[p[2]],matchedTeams[p[3]]))
                matchedTeams[p[0]].playedWith.append(matchedTeams[p[1]])
                matchedTeams[p[1]].playedWith.append(matchedTeams[p[0]])
                matchedTeams[p[2]].playedWith.append(matchedTeams[p[3]])
                matchedTeams[p[3]].playedWith.append(matchedTeams[p[2]])
                for t in [matchedTeams[p[r]] for r in range(4)]:
                    t.canPlay = gap*-1 -1
                break
        for s in schools:
            s.canPlay += 1
if teamsLeft:
    ghosts = 4 - len(teamsLeft)
    for g in range(ghosts):
        teamsLeft.append(Team(-g-1,"Spooky Team"))
perm = list(permutations(range(4)))
for p in perm:
    if matchedTeams[p[0]] not in matchedTeams[p[1]].playedWith and matchedTeams[p[2]] not in matchedTeams[p[3]].playedWith:
        matches.append(Match(matchedTeams[p[0]],matchedTeams[p[1]],matchedTeams[p[2]],matchedTeams[p[3]]))
        break

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
