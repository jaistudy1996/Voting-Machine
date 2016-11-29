
import crusher
import dict
import sys

COMMANDS ={}
VOTERID = 0

def CONF(db, tempVotes, line, logFile):
	db.configure(line[1])
	logFile.write("{}\t{}\t\n".format(line[0], line[1]))

COMMANDS["CONF"] = CONF

def VOTER(db, tempVotes, line, logFile):
	tempVotes.clear()
	global VOTERID
	VOTERID += 1
	tempVotes.append(VOTERID)
	logFile.write("VOTER\n")
	# return False	# Might be used in future

COMMANDS["VOTER"] = VOTER

def VOTE(db, tempVotes, line, logFile):
	tempVotes.append((line[1], line[2]))
	logFile.write("VOTE\t{}\t{}\n".format(line[1], line[2]))

COMMANDS["VOTE"] = VOTE

def CAST(db, tempVotes, line, logFile):
	database = dict.Dict(db)
	database.insert([VOTERID, "t"], str(len(tempVotes) - 1))
	for i in range(1, len(tempVotes)):
		office.append(tempVotes[i][0])
		officeNumber = "o"+str(i)
		candidateNumber = "c"+str(i)
		candidate.append(tempVotes[i][1])
		database.insert([VOTERID, officeNumber], tempVotes[i][0])
		database.insert([VOTERID,  candidateNumber], tempVotes[i][1])
	logFile.write("CAST\t{}\n".format(VOTERID))

COMMANDS["CAST"] = CAST

def report(db, reportFile):
	database = dict.Dict(db, "report")
	tallies = {}


## File read implementation
try:
	fileName = sys.argv[1]
except:
	fileName = "bigeasy.txt"

db = crusher.Broker(fileName)

votesFile = open(fileName, "r")
logFile = open(fileName[:-4]+"-votelog.txt", "w")

tempVotes = []
for line in votesFile:
	#print(line.split()[0])
	line = line.strip()
	COMMANDS[line.split()[0]](db, tempVotes, line.split("\t"), logFile)

votesFile.close()
logFile.close()
db.exit()
