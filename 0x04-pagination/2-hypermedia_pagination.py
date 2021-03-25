#!/usr/bin/env python3
""" Return Hypermedia pagination """
# imports
import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """ Return Tuple from page and page_size """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)

class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Return pagination of Query """
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        query = index_range(page, page_size)
        start, end = query[0], query[1]

        dataset = self.dataset()
        return dataset[start: end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Return Hypermedia pagination """
        pages = math.ceil(len(self.dataset()) / page_size)

        return {
            "page_size": page_size,
            "page": page,
            "data": self.get_page(page, page_size),
            "next_page": page + 1 if page + 1 <= pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": pages
        }


if __name__ == "__main__":
    server = Server()

    print(server.get_hyper(1, 2))
    print("---")
    print(server.get_hyper(2, 2))
    print("---")
    print(server.get_hyper(100, 3))
    print("---")
    print(server.get_hyper(3000, 100))