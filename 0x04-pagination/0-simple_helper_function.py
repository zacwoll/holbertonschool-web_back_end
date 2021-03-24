#!/usr/bin/env python3
""" Form Tuple helper function """
# imports
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """ Return Tuple from page and page_size """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)


if __name__ == "__main__":
    res = index_range(1, 7)
    print(type(res))
    print(res)

    res = index_range(page=3, page_size=15)
    print(type(res))
    print(res)
