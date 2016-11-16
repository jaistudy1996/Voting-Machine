#! /usr/bin/env python3

'''Data strucutre for the reliable systems project'''

import crusher

class Dict:

	def __init__(self, db, name):
		'''DB here belongs to class crusher. Name here is the name of the dictionary used.'''
		self.db = db
		self.internalDict = name

	def insert(self, key, value):
		self.db.store(key, value)

	def select(self, key):
		return self.db.fetch(key)


if __name__ == "__main__":
	db = crusher.Broker("testDict.txt")

	test = Dict(db, "test")
	key = "key1"
	value = "value1"
	test.insert(key, value)
	print(test.select(key))