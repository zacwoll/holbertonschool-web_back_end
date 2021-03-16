#!/usr/bin/env python3
""" Complex types """
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
	""" sum mix list w/ annotations """
	return sum(mxd_lst)