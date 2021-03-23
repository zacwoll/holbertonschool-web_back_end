#!/usr/bin/env python3
""" Basic Cache implementing LIFO """
# imports
BasicCache = __import__('0-basic_cache').BasicCache


class CacheItem:
    """ Implementation of a cache item """
    def __init__(self, key, value):
        """ Cache Item """
        self.key = key
        self.value = value

class LIFOCache(BasicCache):
    """ LIFO (Least In Last Out) implementation of BasicCache """
    def __init__(self):
        """ Constructor """
        super().__init__()
        self.LIFO = []
    
    def put(self, key, item):
        """ Put new item in cache assoc. with key """
        # Do nothing if key is NoneType or item is NoneType
        if (key is None or item is None):
            return

        if (key in self.cache_data):
            self.LIFO = [ci for ci in self.LIFO if ci.key != key]

        self.cache_data[key] = item

        data = CacheItem(key, item)
        self.LIFO.append(data)

        # Length is longer than max capacity, make room
        if len(self.cache_data) > self.MAX_ITEMS:
            discard = self.LIFO.pop(-2)
            print("DISCARD: {}".format(discard.key))
            del self.cache_data[discard.key]

    def get(self, key):
        """ Get item from cache """
        if key is None or key not in self.cache_data:
            return None
        else:
            return self.cache_data[key]

if __name__ == "__main__":
    my_cache = LIFOCache()
    my_cache.put("A", "Hello")
    my_cache.put("B", "World")
    my_cache.put("C", "Holberton")
    my_cache.put("D", "School")
    my_cache.print_cache()
    my_cache.put("E", "Battery")
    my_cache.print_cache()
    my_cache.put("C", "Street")
    my_cache.print_cache()
    my_cache.put("F", "Mission")
    my_cache.print_cache()
    my_cache.put("G", "San Francisco")
    my_cache.print_cache()
