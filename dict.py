#! /usr/bin/env python3

'''
	Data strucutres for the reliable systems project
	
	Author: Jayant Arora

	Team Members: Akshay, Mahir, Robert, Xiao
'''

import crusher
import hashlib
from nltk import FreqDist

VERSIONS = 16  #Just for testing purpose. The actual one is yet to be calculated
'''VERSIONS -1 = 16 : Number of time the key and value pair will be replicated in the database'''

def keyForDb(voterID, version, typeOfKey):
	'''keyForDb: this function makes keys suitable for database.
		the version stands for the verison of the key that is being stored.
		the typeOfKey can be of three types: o -- office, c -- candidate, m -- checksum'''
	return str(voterID)+"-"+str(version)+"-"+str(typeOfKey)


class Dict:

	def __init__(self, db, name):
		'''DB here belongs to class crusher. Name here is the name of the dictionary used.'''
		self.db = db
		self.internalDict = name

	def insertChecksum(self, value):
		'''Calculate md5 checksum of the whole key and value combined'''
		md5_hash = hashlib.md5(value.encode("utf-8")).hexdigest()
		return md5_hash

	def insert(self, key, value):
		'''Key is supposed to be of type list and should be as follows
				key = ["VOTERID", "type(o, c, m)"]'''
		#if(key[1] == "m"):
		#	insertChecksum(key)   ## m should be internal and not added by the main program 
									## needs editing
		for i in range(1, VERSIONS):
			keyToStore = keyForDb(key[0], i, key[1])
			self.db.store(keyToStore, value)
			## checksum store
			checkSumKeyToStore = keyForDb(key[0], i, "m")
			checkSumValueToStore = self.insertChecksum(value)
			self.db.store(checkSumKeyToStore, checkSumValueToStore)

	def select(self, key):
		selection = [] # TO_DO: add voting/checksum check.
		checksumList = [1]
		for i in range(1, VERSIONS):
			keyToSelect = keyForDb(key[0], i, key[1])
			try:
				selection.append(self.db.fetch(keyToSelect))
			except KeyError:
				selection.append("DOES_NOT_EXIST")

		# Voting using NLTK's FreqDist module.
		freq_selection = FreqDist(selection)
		most_common_from_selection = freq_selection.max()

		freq_checksum = FreqDist(checksumList)
		most_common_from_checksum = freq_checksum.max()
		return most_common_from_selection

	def selectChecksum():
		pass
	

if __name__ == "__main__":
	db = crusher.Broker("testDict.txt")
	db.configure("(0,0,0,0,0,0)")
	#db.configure("((1,2,3,4,5,6,7,8))")

	test = Dict(db, "test")
	key = [1, "o"]
	value = "Governor"
	test.insert(key, value)
	try:
		print(test.select(key)) # will need to except unicodeecode error in voting.py
	except UnicodeEncodeError:
		pass
