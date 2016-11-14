#!/usr/bin/env python3

def indexName(dict, key):
    return (dict,"X",key)

def countName(dict):
    return (dict,"N")

def entryName(dict, n):
    return (dict, "E", n)

def statusName(dict):
    return (dict, "S")

class CrusherDict:
    def __init__(self, db, name):
        """Create a set named key in the database."""
        self.db=db
        self.name=name
    def __len__(self):
        try:
            return self.db.fetch(countName(self.name))
        except KeyError:
            return 0
    def __contains__(self,key):
        try:
            self.db.fetch(indexName(self.name,key))
            return True
        except KeyError:
            return False
    def status(self, key, stat=None):
        """Get and optionally set the status of the set."""
        name=statusName(self.name)
        try:
            old=self.db.fetch(name)
        except KeyError:
            old=None
        if stat!=None:
            self.db.store(name,stat)
        return old
    def getKey(self, key, val=None):
        """Get the db key for key from the set.
           If the key is not in the set, it is added to the set.
           The value associated with key is updated unless val is None.
           The key that is used to identify the key in the db
           is returned.
        """
        try:
            dbkey=entryName(self.name,self.db.fetch(indexName(self.name,key)))
            if(val!=None):
                self.db.store(dbkey, (key,val))
            return dbkey
        except KeyError:
            try:
                n=self.db.fetch(countName(self.name))
            except KeyError:
                n=0
            dbkey=entryName(self.name,n)
            self.db.store(dbkey, (key,val))
            self.db.store(indexName(self.name,key), n)
            self.db.store(countName(self.name),n+1)
            return dbkey
    def inc(self, key, val):
        """Increment the value for key from the set.
           If the key is not in the set, it is added to the set with value 1.
           The value is stored in the entry as an annotation.
           The key that is used to identify the key in the db
           is returned.
        """
        try:
            dbkey=entryName(self.name,self.db.fetch(indexName(self.name,key)))
            v=self.db.fetch(dbkey)
            self.db.store(dbkey, (key,v[1]+1,val))
            return dbkey
        except KeyError:
            try:
                n=self.db.fetch(countName(self.name))
            except KeyError:
                n=0
            dbkey=entryName(self.name,n)
            self.db.store(dbkey,(key,1,val))
            self.db.store(indexName(self.name,key), n)
            self.db.store(countName(self.name),n+1)
            return dbkey
    def __iter__(self):
        for i in range(self.__len__()):
            yield self.db.fetch(entryName(self.name,i))

if __name__=="__main__":
    import crusher
    db=crusher.Broker("test_crusherdict")
    test=CrusherDict(db, "test")
    print(test.getKey("Hiddleston","name"))
    print(test.inc("Gov-Muller","voter-809809"))
    for tup in test:
        print(tup)
    db.exit()
