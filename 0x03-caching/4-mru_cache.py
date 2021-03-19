#!/usr/bin/env python3
""" Basic Cache implementing MRU """
# imports
BasicCache = __import__('0-basic_cache').BasicCache
CacheItem = __import__('base_caching').CacheItem


class MRUCacheItem(CacheItem):
    def __init__(self, key, value, age):
        super().__init__(key, value)
        self.age = age

class MRUCache(BasicCache):
    """ MRU (Most Recently Used) implementation of BasicCache """
    def __init__(self):
        """ Constructor """
        super().__init__()
        self.MRU = []
    
    def put(self, key, item):
        """ Put new item in cache assoc. with key """
        # Do nothing if key is NoneType or item is NoneType
        if (key is None or item is None):
            return

        # key is in cache, so remake cache without key
        if key in self.cache_data:
            self.MRU = [ci for ci in self.MRU if ci.key != key]

        # Length will be longer than max capacity, make room
        elif len(self.cache_data) == self.MAX_ITEMS:
            discard = self.MRU[0]
            for x in self.MRU:
                if x.age < discard.age:
                    discard = x
            print("DISCARD: {}".format(discard.key))
            del self.cache_data[discard.key]
            self.MRU.remove(discard)

        # increase age of all items
        for x in self.MRU:
            x.age += 1

        self.cache_data[key] = item
        data = MRUCacheItem(key, item, 0)
        self.MRU.append(data)

    def get(self, key):
        """ Get item from cache """
        if key is None or key not in self.cache_data:
            return None
        else:
            for x in self.MRU:
                if x.key == key:
                    x.age = 0
                else:
                    x.age += 1
            return self.cache_data[key]
