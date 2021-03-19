#!/usr/bin/env python3
""" Basic Cache implementing LIFO """
# imports
BasicCache = __import__('0-basic_cache').BasicCache


class LIFOCache(BasicCache):
    """ LIFO (First In Last Out) implementation of BasicCache """
    def __init__(self):
        """ Constructor """
        super().__init__()
        self.LIFO = []
    
    def put(self, key, item):
        """ Put new item in cache assoc. with key """
        # Do nothing if key is NoneType or item is NoneType
        if (key is None or item is None):
            return

        if key in self.cache_data:
            self.LIFO.remove(key)

        self.cache_data[key] = item
        self.LIFO.append(key)

        # Length is longer than max capacity, make room
        if len(self.cache_data) > self.MAX_ITEMS:
            discard = self.LIFO.pop(-2)
            print("DISCARD: {}".format(discard))
            del self.cache_data[discard]

    def get(self, key):
        """ Get item from cache """
        if key is None or key not in self.cache_data:
            return None
        else:
            return self.cache_data[key]
