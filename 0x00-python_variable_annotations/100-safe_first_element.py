#!/usr/bin/env python3
"""Module with a python script"""
from typing import Sequence, Union, Any


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Adding duck typed anotations"""
    if lst:
        return lst[0]
    else:
        return None
