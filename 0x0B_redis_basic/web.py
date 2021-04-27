#!/usr/bin/env python3
""" Implement an expiring web cache and tracker """
import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()


def count(method: Callable) -> Callable:
    """ Count the number of times a page is accessed """
    @wraps(method)
    def wrapper(*args, **kwargs):
        """ Wrapper """
        r.incr(f"count:{args[0]}")
        page = r.get(args[0])
        if not page:
            page = method(*args, **kwargs)
            r.setex(args[0], 10, page)
        return page
    return wrapper


@count
def get_page(url: str) -> str:
    """ Access a given url using requests """
    return requests.get(url).text
