
import crusher
import dict
import sys

COMMANDS ={}
VOTERID = 0

def CONF(db, tempVotes, line):
	db.configure(line[1])

COMMANDS["CONF"] = CONF

def VOTER(db, tempVotes, line):
	tempVotes.clear()
	global VOTERID
	VOTERID += 1
	tempVotes.append(VOTERID)
	# return False	# Might be used in future

COMMANDS["VOTER"] = VOTER

def VOTE(db, tempVotes, line):
	tempVotes.append((line[1], line[2]))

COMMANDS["VOTE"] = VOTE

def CAST(db, tempVotes, line):
	database = dict.Dict(db)
	id = tempVotes[0]
	office = []
	candidate = []
	for i in range(1, len(tempVotes)):
		office.append(tempVotes[i][0])
		candidate.append(tempVotes[i][1])
		database.insert([VOTERID, "o"], tempVotes[i][0])
		database.insert([VOTERID,  "c"], tempVotes[i][1])
	print(office)
	print(candidate)

COMMANDS["CAST"] = CAST

## File read implementation
try:
	fileName = sys.argv[1]
except:
	fileName = "bigeasy.txt"

db = crusher.Broker(fileName)

file = open(fileName, "r")

tempVotes = []
for line in file:
	#print(line.split()[0])
	line = line.strip()
	COMMANDS[line.split()[0]](db, tempVotes, line.split("\t"))

file.close()
db.exit()
