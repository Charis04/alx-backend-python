#!usr/bin/env python3
"""Write a coroutine called async_generator that takes no arguments."""

import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
    Asynchronous generator that yields a random number between 0 and 10,
    after waiting 1 second, for a total of 10 times.
    """
    for _ in range(10):
        await asyncio.sleep(1)  # Asynchronously wait for 1 second
        yield random.random() * 10  # Yield a random float between 0 and 10
