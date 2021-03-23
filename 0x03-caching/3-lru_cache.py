#!/usr/bin/env python3
""" Basic Cache implementing LRU """
# imports
BasicCache = __import__('0-basic_cache').BasicCache


class CacheItem:
    """ Implementation of a cache item """
    def __init__(self, key, value):
        """ Cache Item """
        self.key = key
        self.value = value

class LRUCacheItem(CacheItem):
    """ Implementation of a Least Recently Used cache item """
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

if __name__ == "__main__":
    my_cache = LRUCache()
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
    my_cache.put("J", "J")
    my_cache.print_cache()
    my_cache.put("K", "K")
    my_cache.print_cache()
