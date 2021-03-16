#!/usr/bin/env python3
""" Execute multiple coroutines at the same time with async """
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random

async def wait_n(n: int, max_delay: int):
    """ Generate list of delay times """
    return [await wait_random(max_delay) for _ in range(n)]
