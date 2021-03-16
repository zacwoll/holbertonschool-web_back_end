#!/usr/bin/env python3
""" Generates asyncio.Task list """
import asyncio
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int):
    """ Generates asyncio.Task list of delays """
    tasks = []
    for _ in range(n):
        tasks.append(await task_wait_random(max_delay))
    return tasks
