import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-input')
parser.add_argument('-n')
args = parser.parse_args()
print(args)

class Match:
    def __init__(self, num, b1, b2, g1, g2):
        self.num =  num
        self.b1 = b1
        self.b2 = b2
        self.g1 = g1
        self.g2 = g2

class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.lastmatch = 0
        self.numPlayed = 0

schools = {}
totalMatches = args.n

def process(line):
    values = line.rstrip().split(",")
    schools[values[0]] = Team(values[0], values[1])

with open(args.input) as f:
    for line in f:
        process(line)
print(schools)

#for i in totalMatches:
