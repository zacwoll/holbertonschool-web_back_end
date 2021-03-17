#!/usr/bin/env python3
""" Measure time of function """
wait_n = __import__('1-concurrent_coroutines').wait_n
import asyncio
import time


def measure_time(n: int, max_delay: int) -> float:
    """ Times the function call """
    s = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    elapsed = time.perf_counter() - s
    return elapsed / n
