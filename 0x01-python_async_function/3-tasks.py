#!/usr/bin/env python3
""" Create an asyncio Task """
wait_random = __import__('0-basic_async_syntax').wait_random
import asyncio


def task_wait_random(max_delay: int):
    """ Creates an asyncio.Task out of wait_random from task 0 """
    return asyncio.create_task(wait_random(max_delay))
