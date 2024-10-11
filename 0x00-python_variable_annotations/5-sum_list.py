#!/usr/bin/env python3
from typing import List
"""
This module provides a function to sum a list of floats.
"""


def sum_list(input_list: List[float]) -> float:
    """
    Sum a list of floats and return the result

    Args:
      input_list (List[float]): a list of floats

    Returns:
      float: the sum of the list of floats
    """
    return sum(input_list)
