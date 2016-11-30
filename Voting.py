#! /usr/bin/env python3

"""
    Voting.py implements dict.py as its datastructure.
    Team Members: Jayant Arora, Akshay Singh, Muhtasim Mahir, Robert Elliot, Xiaocan Dong
"""

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
    # return False  # Might be used in future

COMMANDS["VOTER"] = VOTER

def VOTE(db, tempVotes, line, logFile):
    tempVotes.append((line[1], line[2]))
    logFile.write("VOTE\t{}\t{}\n".format(line[1], line[2]))

COMMANDS["VOTE"] = VOTE

def CAST(db, tempVotes, line, logFile):
    database = dict.Dict(db)
    database.insert([VOTERID, "t"], str(len(tempVotes) - 1))
    for i in range(1, len(tempVotes)):
        officeNumber = "o"+str(i)
        candidateNumber = "c"+str(i)
        database.insert([VOTERID, officeNumber], tempVotes[i][0])
        database.insert([VOTERID,  candidateNumber], tempVotes[i][1])
    logFile.write("CAST\t{}\n".format(VOTERID))

COMMANDS["CAST"] = CAST

def report(db, reportFile):
    database = dict.Dict(db, "report")
    tallies = {}
    for i in range(1, VOTERID+1):
        try:    
            totalVotes = database.select([i, "t"])
            tallies[i] = []
            tallies[i].append(totalVotes)
            try:
                # print(totalVotes) # DEBUG
                for j in range(1, int(totalVotes)+1):
                    officeNumber = "o"+str(j)
                    candidateNumber = "c"+str(j)
                    office = database.select([i, officeNumber])
                    candidate = database.select([i, candidateNumber])
                    # print((office, candidate))  # DEBUG
                    tallies[i].append((office, candidate))
            except NameError as e:
                print("Exception -1 in report func: ", e)
                i -= 1
            except ValueError as e:
                print("Exception -2 in report func: ", e)
                continue
        except dict.ChecksumDoesNotMatchError:
            continue

    final = {}
    for keys in tallies:
        for i in range(1, len(tallies[keys])):
            if (tallies[keys][i][0], tallies[keys][i][1]) in final:
                final[(tallies[keys][i][0], tallies[keys][i][1])] += 1
            else:
                final[(tallies[keys][i][0], tallies[keys][i][1])] = 1
        # line = str(keys) + "\t" + str(tallies[keys]) + "\n"
        # line = str(final[keys]) + "\n"
    
    reportFile.write("VOTERS\t", VOTERID)
    for keys in final:
        line = "TALLY" + "\t" + str(keys[0]) + "\t" + str(keys[1]) + "\t" + str(final[keys]) + "\n"
        # line = str(keys) + "\n"
        reportFile.write(line)
    print(tallies)
    print(final)


def INQ(db, tempVotes, line, inqfile):
    database = dict.Dict(db, "inquiry")
    tallies = {}
    for i in range(1, VOTERID):
        try:    
            totalVotes = database.select([i, "t"])
            tallies[i] = []
            tallies[i].append(i)
            tallies[i].append(totalVotes)
            try:
                # print(totalVotes) # DEBUG
                for j in range(1, int(totalVotes)+1):
                    officeNumber = "o"+str(j)
                    candidateNumber = "c"+str(j)
                    office = database.select([i, officeNumber])
                    candidate = database.select([i, candidateNumber])
                    # print((office, candidate))  # DEBUG
                    tallies[i].append((office, candidate))
            except NameError as e:
                print("Exception -1 in INQ func: ", e)
                i -= 1
            except ValueError as e:
                print("Exception -2 in INQ func: ", e)
                continue
        except dict.ChecksumDoesNotMatchError:
            continue


    for keys in tallies:
        if(line[1] == tallies[keys][0]):
            inqfile.write("VOTER\n")
            print(tallies[keys])
            for index in range(2, len(tallies[keys])):
                # line = str("VOTE\t" + str(index) + "\n")
                line2 = str("VOTE\t" + tallies[keys][index][0] + "\t" + tallies[keys][index][1] + "\n") 
                # inqfile.write(line)
                inqfile.write(line2)
            inqfile.write(str("CAST\t" + str(tallies[keys][0]) + "\n"))
        else:
            continue
COMMANDS["INQ"] = INQ


## File read implementation
try:
    fileName = sys.argv[1]
except:
    fileName = "bigeasy.txt"

db = crusher.Broker(fileName)

votesFile = open(fileName, "r")
logFile = open(fileName[:-4]+"-votelog.txt", "w")
resultFile = open(fileName[:-4]+"-results.txt", "w")
inqfile = open(fileName[:-4]+"-inqries.txt", "w")

tempVotes = []
for line in votesFile:
    #print(line.split()[0])
    line = line.strip()
    COMMANDS[line.split()[0]](db, tempVotes, line.split("\t"), logFile)

report(db, resultFile)
# INQ(db, tempVotes, "", inqfile)
resultFile.close()
votesFile.close()
logFile.close()
inqfile.close()
db.exit()
