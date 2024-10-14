#!/usr/bin/env python3
"""
An async routine called wait_n that takes in 2 int arguments (in this order):
n and max_delay. You will spawn wait_random n times with the specified
max_delay.
"""

import asyncio

wait_r = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list[float]:
    """
wait_n should return the list of all the delays (float values).
The list of the delays should be in ascending order without using sort()
 because of concurrency.
    """
     # Create a list of tasks, each waiting for a random delay
    tasks = [asyncio.create_task(wait_r(max_delay)) for _ in range(n)]

    # Collect completed results as they finish
    delays = []
    for task in asyncio.as_completed(tasks):
        result = await task
        delays.append(result)

    return delays