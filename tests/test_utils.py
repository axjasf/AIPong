"""Test utilities and helper functions."""

from typing import Tuple, Union
import numpy as np

# Type alias for numeric types
Numeric = Union[int, float, np.number]

def assert_float_equal(a: Numeric, b: Numeric, epsilon: float = 1e-10, msg: str = "") -> None:
    """Assert that two floating point numbers are equal within epsilon.
    
    Args:
        a: First number
        b: Second number
        epsilon: Maximum allowed difference
        msg: Optional message to display on failure
    """
    assert abs(float(a) - float(b)) < epsilon, f"{msg} (diff: {abs(float(a) - float(b))})"

def assert_floats_equal(a: Tuple[Numeric, ...], b: Tuple[Numeric, ...], epsilon: float = 1e-10, msg: str = "") -> None:
    """Assert that two tuples of floating point numbers are equal within epsilon.
    
    Args:
        a: First tuple of numbers
        b: Second tuple of numbers
        epsilon: Maximum allowed difference
        msg: Optional message to display on failure
    """
    assert len(a) == len(b), f"{msg} (lengths differ: {len(a)} != {len(b)})"
    for i, (x, y) in enumerate(zip(a, b)):
        assert abs(float(x) - float(y)) < epsilon, f"{msg} at index {i} (diff: {abs(float(x) - float(y))})"

def assert_float_not_equal(a: Numeric, b: Numeric, epsilon: float = 1e-10, msg: str = "") -> None:
    """Assert that two floating point numbers are not equal within epsilon.
    
    Args:
        a: First number
        b: Second number
        epsilon: Maximum allowed difference
        msg: Optional message to display on failure
    """
    assert abs(float(a) - float(b)) >= epsilon, f"{msg} (diff: {abs(float(a) - float(b))})"

def assert_floats_not_equal(a: Tuple[Numeric, ...], b: Tuple[Numeric, ...], epsilon: float = 1e-10, msg: str = "") -> None:
    """Assert that two tuples of floating point numbers are not equal within epsilon.
    
    Args:
        a: First tuple of numbers
        b: Second tuple of numbers
        epsilon: Maximum allowed difference
        msg: Optional message to display on failure
    """
    assert len(a) == len(b), f"{msg} (lengths differ: {len(a)} != {len(b)})"
    any_different = False
    for x, y in zip(a, b):
        if abs(float(x) - float(y)) >= epsilon:
            any_different = True
            break
    assert any_different, f"{msg} (all values are equal within {epsilon})" 