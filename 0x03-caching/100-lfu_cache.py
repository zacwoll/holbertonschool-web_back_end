#!/usr/bin/env python3
""" Basic Cache implementing LFU """
# imports
BasicCache = __import__('0-basic_cache').BasicCache
CacheItem = __import__('base_caching').CacheItem


class LFUCacheItem(CacheItem):
    def __init__(self, key, value, age, freq):
        super().__init__(key, value)
        self.age = age
        self.freq = freq

    def updateItem(self, value):
        self.value = value
        self.age = 0
        self.freq += 1

class LFUCache(BasicCache):
    """ LFU (Least Recently Used) implementation of BasicCache """
    def __init__(self):
        """ Constructor """
        super().__init__()
        self.LFU = []
    
    def put(self, key, item):
        """ Put new item in cache assoc. with key """
        # Do nothing if key is NoneType or item is NoneType
        if (key is None or item is None):
            return

        # If Key exists, update Cache Item
        if key in self.cache_data:
            for ci in self.LFU:
                if ci.key is key:
                    ci.updateItem(item)
        else:
            # Length will be longer than max capacity, make room
            if len(self.cache_data) == self.MAX_ITEMS:

                # Determine discarded cache item
                discard = self.LFU[0]
                for x in self.LFU:
                    if x.freq < discard.freq or \
                        x.freq == discard.freq and x.age > discard.age:
                        discard = x

                # Discard Cache Item
                print("DISCARD: {}".format(discard.key))
                del self.cache_data[discard.key]
                self.LFU.remove(discard)

            # Add new Cache Item
            data = LFUCacheItem(key, item, 0, 0)
            self.LFU.append(data)

        # increase age of all items
        for x in self.LFU:
            x.age += 1

        self.cache_data[key] = item

    def get(self, key):
        """ Get item from cache """
        if key is None or key not in self.cache_data:
            return None
        else:
            for x in self.LFU:
                if x.key == key:
                    x.age = 0
                    x.freq += 1
                else:
                    x.age += 1
            return self.cache_data[key]
