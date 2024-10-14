#!/usr/bin/env python3
"""
A program that creates an async task
"""

import asyncio

wait_r = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
A function (do not create an async function, use the regular function syntax
to do this) task_wait_random that takes an integer max_delay and returns a
asyncio.Task.
    """
    return asyncio.create_task(wait_r(max_delay))
