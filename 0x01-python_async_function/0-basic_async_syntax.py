#!/usr/bin/env python3
""" Basic Async Delay """
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """ Awaits random delay between 0 & max-delay """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
