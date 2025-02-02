"""Test suite for game types."""

import pytest
import pygame
from src.game_types import BallState, PaddleState


def test_ball_state_initialization():
    """Test ball state initialization with default values."""
    state = BallState()
    assert state.x == 0
    assert state.y == 0
    assert state.prev_x == 0
    assert isinstance(state.rect, pygame.Rect)
    assert not state.passed_paddle
    assert not state.hit_paddle


def test_ball_state_custom_values():
    """Test ball state initialization with custom values."""
    rect = pygame.Rect(10, 20, 30, 40)
    state = BallState(x=5.0, y=10.0, prev_x=4.0, rect=rect, passed_paddle=True, hit_paddle=True)
    assert state.x == 5.0
    assert state.y == 10.0
    assert state.prev_x == 4.0
    assert state.rect == rect
    assert state.passed_paddle
    assert state.hit_paddle


def test_paddle_state_initialization():
    """Test paddle state initialization with default values."""
    state = PaddleState()
    assert state.left_y == 0
    assert state.right_y == 0
    assert state.left_hits == 0
    assert state.right_hits == 0


def test_paddle_state_custom_values():
    """Test paddle state initialization with custom values."""
    state = PaddleState(left_y=100.0, right_y=200.0, left_hits=3, right_hits=2)
    assert state.left_y == 100.0
    assert state.right_y == 200.0
    assert state.left_hits == 3
    assert state.right_hits == 2 