#!/usr/bin/env python3
""" Basic Cache implementing LRU """
# imports
BasicCache = __import__('0-basic_cache').BasicCache
CacheItem = __import__('base_caching').CacheItem


class LRUCacheItem(CacheItem):
    def __init__(self, key, value, age):
        super().__init__(key, value)
        self.age = age

class LRUCache(BasicCache):
    """ LRU (Least Recently Used) implementation of BasicCache """
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
            self.LRU = [ci for ci in self.LRU if ci.key != key]

        # increase age of all items
        for x in self.LRU:
            x.age += 1

        self.cache_data[key] = item
        data = LRUCacheItem(key, item, 0)
        self.LRU.append(data)

        # Length is longer than max capacity, make room
        if len(self.cache_data) > self.MAX_ITEMS:
            discard = self.LRU[0]
            for x in self.LRU:
                if x.age > discard.age:
                    discard = x
            print("DISCARD: {}".format(discard.key))
            del self.cache_data[discard.key]
            self.LRU.remove(discard)

    def get(self, key):
        """ Get item from cache """
        if key is None or key not in self.cache_data:
            return None
        else:
            for x in self.LRU:
                if x.key == key:
                    x.age = 0
                else:
                    x.age += 1
            return self.cache_data[key]
