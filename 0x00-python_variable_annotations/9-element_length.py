#!/usr/bin/env python3
""" duck type """
from typing import Iterable, Sequence, Tuple, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ some function """
    return [(i, len(i)) for i in lst]