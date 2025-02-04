"""Test suite for game types."""

import pytest
import pygame
from src.game_types import BallState, PaddleState
from .test_utils import assert_float_equal


def test_ball_state_initialization():
    """Test ball state initialization."""
    state = BallState()
    assert_float_equal(state.x, 0.0, msg="Initial x should be 0")
    assert_float_equal(state.y, 0.0, msg="Initial y should be 0")
    assert_float_equal(state.prev_x, 0.0, msg="Initial prev_x should be 0")
    assert isinstance(state.rect, pygame.Rect)
    assert not state.passed_paddle
    assert not state.hit_paddle


def test_ball_state_custom_values():
    """Test ball state with custom values."""
    state = BallState(x=5.0, y=10.0, prev_x=4.0)
    assert_float_equal(state.x, 5.0, msg="x should match input")
    assert_float_equal(state.y, 10.0, msg="y should match input")
    assert_float_equal(state.prev_x, 4.0, msg="prev_x should match input")
    assert isinstance(state.rect, pygame.Rect)
    assert not state.passed_paddle
    assert not state.hit_paddle


def test_paddle_state_initialization():
    """Test paddle state initialization."""
    state = PaddleState()
    assert_float_equal(state.left_y, 0.0, msg="Initial left_y should be 0")
    assert_float_equal(state.right_y, 0.0, msg="Initial right_y should be 0")
    assert state.left_hits == 0
    assert state.right_hits == 0


def test_paddle_state_custom_values():
    """Test paddle state with custom values."""
    state = PaddleState(left_y=100.0, right_y=200.0)
    assert_float_equal(state.left_y, 100.0, msg="left_y should match input")
    assert_float_equal(state.right_y, 200.0, msg="right_y should match input")
    assert state.left_hits == 0
    assert state.right_hits == 0 