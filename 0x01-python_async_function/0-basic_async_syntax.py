#!/usr/bin/env python3
"""Module with a python script"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Function that waits for the delay"""
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
