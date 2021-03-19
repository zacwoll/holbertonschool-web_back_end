#!/usr/bin/env python3
""" Basic Cache implementing MRU """
# imports
BasicCache = __import__('0-basic_cache').BasicCache


class MRUCache(BasicCache):
    """ MRU (First In Last Out) implementation of BasicCache """
    def __init__(self):
        """ Constructor """
        super().__init__()
        self.MRU = []
    
    def put(self, key, item):
        """ Put new item in cache assoc. with key """
        # Do nothing if key is NoneType or item is NoneType
        if (key is None or item is None):
            return

        # key is in cache, so update cache without key
        if key in self.cache_data:
            self.MRU = [k for k in self.MRU if key not in k[0]]
        # Length will be longer than max capacity, make room
        elif len(self.cache_data) == self.MAX_ITEMS:
            discard = self.MRU[0]
            for x in self.MRU:
                if x[1] < discard[1]:
                    discard = x
            print("DISCARD: {}".format(discard[0]))
            del self.cache_data[discard[0]]
            self.MRU.remove(discard)

        # increase age of all items
        for x in self.MRU:
            x[1] += 1

        self.cache_data[key] = item
        self.MRU.append([key, 0])

    def get(self, key):
        """ Get item from cache """
        if key is None or key not in self.cache_data:
            return None
        else:
            for x in self.MRU:
                if x[0] == key:
                    x[1] = 0
                else:
                    x[1] += 1
            return self.cache_data[key]
