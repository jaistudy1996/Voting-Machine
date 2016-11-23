
import crusher
import dict
import sys

COMMANDS ={}

def CONF():
	print("CONF func")
	pass
COMMANDS["CONF"] = CONF

def VOTE():
	print("VOTE func")
	pass
COMMANDS["VOTE"] = VOTE

def VOTER():
	print("VOTER func")
	pass
COMMANDS["VOTER"] = VOTER

def CAST():
	print("CAST func")
	pass
COMMANDS["CAST"] = CAST

## File read implementation
try:
	fileName = sys.argv[1]
except:
	fileName = "bigeasy.txt"

file = open(fileName, "r")

for line in file:
	#print(line.split()[0])
	COMMANDS[line.split()[0]]()
