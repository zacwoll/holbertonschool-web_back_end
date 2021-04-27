#!/usr/bin/env python3
""" Exercise in using Redis """
from functools import wraps
import redis
from typing import Callable, Optional, Union
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """ Count the number of times a method is called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Use the redis instance of the wrapped method to track calls """
        self._redis.incr(key, 1)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Store the history of transactions with the db """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Broker with the redis instance """
        self._redis.rpush(method.__qualname__ + ':inputs', str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ':outputs', output)
        return output
    return wrapper


def replay(method: Callable):
    """ Display a history of calls of a particular function """
    r = redis.Redis()
    name = method.__qualname__
    count = int(r.get(name))
    inputs = r.lrange(f'{name}:inputs', 0, -1)
    inputs = [input.decode('utf-8') for input in inputs]
    outputs = r.lrange(f'{name}:outputs', 0, -1)
    outputs = [output.decode('utf-8') for output in outputs]
    print(f"{name} was called {count} times:")
    for input, output in zip(inputs, outputs):
        print(f"{name}(*{input}) -> {output}")


class Cache:
    """ Cache class """
    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store in redis cache """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float]:
        """ Get Data from storage """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, data: str) -> str:
        """ Get Data converted to str """
        return self._redis.get(data).decode('utf-8')

    def get_int(self, data: str) -> int:
        """ Get Data converted to int """
        return int(self._redis.get(data))
