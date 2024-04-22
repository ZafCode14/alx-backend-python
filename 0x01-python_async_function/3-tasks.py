#!/usr/bin/env python3
"""Module with a python script"""

from asyncio import Task, create_task

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> Task:
    """Function that reutrns the task"""
    task = create_task(wait_random(max_delay))
    return task
