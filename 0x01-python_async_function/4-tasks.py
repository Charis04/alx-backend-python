#!/usr/bin/env python3
"""
An async routine called task_wait_n that takes in 2 int arguments 
(in this order):
n and max_delay. You will spawn wait_random n times with the specified
max_delay.
"""

import asyncio
from typing import List

task_wait_r = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
task_wait_n should return the list of all the delays (float values).
The list of the delays should be in ascending order without using sort()
because of concurrency.
    """
    tasks = [task_wait_r(max_delay) for _ in range(n)]
    delay = await asyncio.gather(*tasks)
    return sorted(delay)
