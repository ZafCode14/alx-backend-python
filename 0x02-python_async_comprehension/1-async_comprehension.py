#!/usr/bin/env python3
"""Module with a python script"""

import asyncio
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """Coroutine that returns the 10 random numbers"""
    compr = [i async for i in async_generator()]
    return compr
