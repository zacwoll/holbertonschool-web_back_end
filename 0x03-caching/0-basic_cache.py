#!/usr/bin/env python3
""" Implement BasicCache Object """
# imports
BasicCaching = __import__('base_caching').BaseCaching


class BasicCache(BasicCaching):
    """ BasicCache implements BasicCaching object given """
    def put(self, key, item):
        """ Put new item in cache assoc. with key """
        if (key is not None and item is not None):
            self.cache_data[key] = item

    def get(self, key):
        """ Get item from cache """
        if key is None or key not in self.cache_data:
            return None
        else:
            return self.cache_data[key]
