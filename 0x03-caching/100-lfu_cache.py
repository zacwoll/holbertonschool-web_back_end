#!/usr/bin/env python3
""" Basic Cache implementing LFU """
# imports
BasicCache = __import__('0-basic_cache').BasicCache


class CacheItem:
    """ Implementation of a cache item """
    def __init__(self, key, value):
        """ Cache Item """
        self.key = key
        self.value = value

class LFUCacheItem(CacheItem):
    """ Least Frequently Used Inherits from CacheItem """
    def __init__(self, key, value, age, freq):
        """ Constructor """
        super().__init__(key, value)
        self.age = age
        self.freq = freq

    def updateItem(self, value):
        """ Update a cache item """
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

if __name__ == "__main__":
    my_cache = LFUCache()
    my_cache.put("A", "Hello")
    my_cache.put("B", "World")
    my_cache.put("C", "Holberton")
    my_cache.put("D", "School")
    my_cache.print_cache()
    print(my_cache.get("B"))
    my_cache.put("E", "Battery")
    my_cache.print_cache()
    my_cache.put("C", "Street")
    my_cache.print_cache()
    print(my_cache.get("A"))
    print(my_cache.get("B"))
    print(my_cache.get("C"))
    my_cache.put("F", "Mission")
    my_cache.print_cache()
    my_cache.put("G", "San Francisco")
    my_cache.print_cache()
    my_cache.put("H", "H")
    my_cache.print_cache()
    my_cache.put("I", "I")
    my_cache.print_cache()
    print(my_cache.get("I"))
    print(my_cache.get("H"))
    print(my_cache.get("I"))
    print(my_cache.get("H"))
    print(my_cache.get("I"))
    print(my_cache.get("H"))
    my_cache.put("J", "J")
    my_cache.print_cache()
    my_cache.put("K", "K")
    my_cache.print_cache()
    my_cache.put("L", "L")
    my_cache.print_cache()
    my_cache.put("M", "M")
    my_cache.print_cache()
