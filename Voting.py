
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
	pass

COMMANDS["VOTE"] = VOTE

def CAST(db, tempVotes, line):
	print(tempVotes)

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
	COMMANDS[line.split()[0]](db, tempVotes, line.split())

file.close()
db.exit()
