#!/usr/bin/env python3
"""Module with a python script"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Function that multilies a float"""
    def function(n: float) -> float:
        """Function that multiplies n by multiplier"""
        return float(n * multiplier)

    return function
