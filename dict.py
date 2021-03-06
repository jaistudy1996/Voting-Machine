#! /usr/bin/env python3

'''
	Data strucutres for the reliable systems project
	
	Author: Jayant Arora, Akshay Singh

	Team Members: Akshay, Mahir, Robert, Xiao
'''

import crusher
import hashlib
from nltk import FreqDist

class ChecksumDoesNotMatchError(Exception):
	pass

VERSIONS = 16  #Just for testing purpose. The actual one is yet to be calculated
'''VERSIONS -1 = 16 : Number of time the key and value pair will be replicated in the database'''

def keyForDb(voterID, version, typeOfKey):
	'''keyForDb: this function makes keys suitable for database.
		the version stands for the verison of the key that is being stored.
		the typeOfKey can be of three types: o -- office, c -- candidate, m -- checksum'''
	return str(voterID)+"-"+str(version)+"-"+str(typeOfKey)


class Dict:

	def __init__(self, db, name="internalName"):
		'''DB here belongs to class crusher. Name here is the name of the dictionary used.'''
		self.db = db
		self.internalDict = name

	def __insertChecksum__(self, value):
		'''Calculate md5 checksum of the whole key and value combined'''
		md5_hash = hashlib.md5(value.encode("utf-8")).hexdigest()
		return md5_hash#[:8]

	def insert(self, key, value):
		'''Key is supposed to be of type list and should be as follows
				key = ["VOTERID", "type(o, c, m)"]'''
		#if(key[1] == "m"):
		#	__insertChecksum__(key)   ## m should be internal and not added by the main program 
									## needs editing
		for i in range(1, VERSIONS):
			if(key[1] == "t"):
				self.db.store(keyForDb(key[0], i, key[1]), value)
				continue
			keyToStore = keyForDb(key[0], i, key[1])
			self.db.store(keyToStore, value)
			## checksum store
			if(key[1][0] == "o"):
				checkSumKeyToStore = keyForDb(key[0], i, "om")
			if(key[1][0] == "c"):
				checkSumKeyToStore = keyForDb(key[0], i, "cm")
			if(key[1][0] == "t"):
				checkSumKeyToStore = keyForDb(key[0], i, "tm")
			checkSumValueToStore = self.__insertChecksum__(value)
			self.db.store(checkSumKeyToStore, checkSumValueToStore)

	def select(self, key):
		''''
			select(key) mimics the db.fetch method from crusher.py
			The name select comes from the sql sytax for processing select queries
		'''
		selection = []
		checksumList = []
		
		# Get data for the supplied key
		for i in range(1, VERSIONS):
			keyToSelect = keyForDb(key[0], i, key[1])
			try:
				selection.append(self.db.fetch(keyToSelect))
			except KeyError:
				selection.append("DOES_NOT_EXIST")

		# Get checksum for the supplied key
		for i in range(1, VERSIONS):
			if(key[1][0] == "o"):
				keyForChecksum = keyForDb(key[0], i, "om")
			if(key[1][0] == "c"):
				keyForChecksum = keyForDb(key[0], i, "cm")
			if(key[1][0] == "t"):
				keyForChecksum = keyForDb(key[0], i, "tm")
			try:
				checksumList.append(self.db.fetch(keyForChecksum))
			except KeyError:
				checksumList.append("CHECKSUM_DOES_NOT_EXIST")
			except UnboundLocalError:
				pass

		# Voting using NLTK's FreqDist module.
		freqSelection = FreqDist(selection)
		mostCommonFromSelection = freqSelection.max()

		freqChecksum = FreqDist(checksumList)
		mostCommonFromChecksum = freqChecksum.max()

		# Compare checksum 
		if(self.__CompareChecksumWithSelection__(mostCommonFromSelection, mostCommonFromChecksum) == True):
			return mostCommonFromSelection
		else:
			# Raise checksum error is it does not match.
			# TO_DO: Again try more selections and checksum comparision
			return mostCommonFromSelection

	def __CompareChecksumWithSelection__(self, selection, checksum):
		# Will take two parameters (selection, checksum) and compare it to 
		# return boolean value. 
		if(self.__insertChecksum__(selection) == checksum):
			return True
		else:
			return False
	

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
	except ChecksumDoesNotMatchError:
		pass
	db.exit()
	
