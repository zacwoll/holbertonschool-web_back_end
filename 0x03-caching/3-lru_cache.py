#!/usr/bin/env python3
""" Basic Cache implementing LRU """
# imports
BasicCache = __import__('0-basic_cache').BasicCache


class LRUCache(BasicCache):
    """ LRU (First In Last Out) implementation of BasicCache """
    def __init__(self):
        """ Constructor """
        super().__init__()
        self.LRU = []
    
    def put(self, key, item):
        """ Put new item in cache assoc. with key """
        # Do nothing if key is NoneType or item is NoneType
        if (key is None or item is None):
            return

        if key in self.cache_data:
            self.LRU = [k for k in self.LRU if key not in k[0]]

        # increase age of all items
        for x in self.LRU:
            x[1] += 1

        self.cache_data[key] = item
        self.LRU.append([key, 0])

        # Length is longer than max capacity, make room
        if len(self.cache_data) > self.MAX_ITEMS:
            discard = self.LRU[0]
            for x in self.LRU:
                if x[1] > discard[1]:
                    discard = x
            print("DISCARD: {}".format(discard[0]))
            del self.cache_data[discard[0]]
            self.LRU.remove(discard)

    def get(self, key):
        """ Get item from cache """
        if key is None or key not in self.cache_data:
            return None
        else:
            for x in self.LRU:
                if x[0] == key:
                    x[1] = 0
                else:
                    x[1] += 1
            return self.cache_data[key]
