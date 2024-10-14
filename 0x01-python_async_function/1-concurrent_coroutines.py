#!/usr/bin/env python3
"""
An async routine called wait_n that takes in 2 int arguments (in this order):
n and max_delay. You will spawn wait_random n times with the specified
max_delay.
"""

import asyncio
from typing import List

wait_r = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
wait_n should return the list of all the delays (float values).
The list of the delays should be in ascending order without using sort()
 because of concurrency.
    """
    delay = await asyncio.gather(*(wait_r(max_delay) for i in range(n)))
    return delay
