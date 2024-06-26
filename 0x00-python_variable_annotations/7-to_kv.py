#!/usr/bin/env python3
"""Module with python script"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """function that returns a tuple"""
    return (k, float(v * v))
