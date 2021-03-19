# 0x03 Caching

Post-Edit Edit:
I decided I was correct in thinking that the index-based logic was hard to read and after talking with my Web Stack Lead, it was worth updating. I placed a CacheItem class in base_caching and implemented it across the files to make their logic flow better, I'm proud of the changes made and how much easier it was to read what was going on but also debugging was easier, further strengthening the idea that a more robust data structure was better.

Post-Tasks Edit:
I wanted to add a side note, I implemented the business logic of these caches with a simple list, but I found that created issues later on. In the future, and maybe if I redo these problems, I would make the logic based around objects instead, which would allow me to directly use the values I was looking for as properties of the object. Too often I found myself using item[0] as a key and item[1] as an age (or a count when I misread one of my instructions as a Least-Used Cache instead of a Least-Recently-Used Cache). I think creating this cache and implementing these lists as objects that hold props like key and age would make the logic flow a lot better, but I think perhaps it's beyond the scope of this project.

Parent class BaseCaching
All your classes must inherit from BaseCaching defined below:

```
$ cat base_caching.py
#!/usr/bin/python3
""" BaseCaching module
"""

class BaseCaching():
    """ BaseCaching defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """
    MAX_ITEMS = 4

    def __init__(self):
        """ Initiliaze
        """
        self.cache_data = {}

    def print_cache(self):
        """ Print the cache
        """
        print("Current cache:")
        for key in sorted(self.cache_data.keys()):
            print("{}: {}".format(key, self.cache_data.get(key)))

    def put(self, key, item):
        """ Add an item in the cache
        """
        raise NotImplementedError("put must be implemented in your cache class")

    def get(self, key):
        """ Get an item by key
        """
        raise NotImplementedError("get must be implemented in your cache class")
```

