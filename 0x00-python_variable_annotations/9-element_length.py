#!/usr/bin/env python3
"""Module with a python script"""
from typing import List, Tuple, Iterable, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Function that return a list"""
    return [(i, len(i)) for i in lst]
