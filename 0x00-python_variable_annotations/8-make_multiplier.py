#!/usr/bin/env python3
""" Complex types """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
	""" Return a multiplier function w/ annotations"""
	def foo(n: float) -> float:
		""" multiplier function """
		return n * multiplier

	return foo