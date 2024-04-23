#!/usr/bin/env python3
"""Module with a python script"""

from typing import Generator
import asyncio
import random


async def async_generator() -> Generator[float, None, None]:
    """Function with a async generator"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
    
