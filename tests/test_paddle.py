"""Test suite for paddle movement and boundaries."""

import pytest
import pygame
from src.paddle import Paddle
from src.constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED
)


@pytest.fixture
def paddle() -> Paddle:
    """Create a paddle fixture for tests."""
    pygame.init()
    x = 100
    y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2)
    return Paddle(x, y, GAME_AREA_TOP, GAME_AREA_TOP + GAME_AREA_HEIGHT)


def test_paddle_initialization(paddle: Paddle) -> None:
    """Test paddle is initialized with correct position and properties."""
    assert paddle.x == 100
    assert paddle.y == float(GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2))
    assert paddle.rect.width == PADDLE_WIDTH
    assert paddle.rect.height == PADDLE_HEIGHT


def test_paddle_movement_up(paddle: Paddle) -> None:
    """Test paddle moves up correctly."""
    initial_y = paddle.get_y()
    paddle.move(up=True)
    assert paddle.get_y() < initial_y
    assert paddle.get_y() == initial_y - PADDLE_SPEED


def test_paddle_movement_down(paddle: Paddle) -> None:
    """Test paddle moves down correctly."""
    initial_y = paddle.get_y()
    paddle.move(up=False)
    assert paddle.get_y() > initial_y
    assert paddle.get_y() == initial_y + PADDLE_SPEED


def test_paddle_top_boundary(paddle: Paddle) -> None:
    """Test paddle stops at top boundary."""
    # Move paddle to top boundary
    paddle.set_y(GAME_AREA_TOP)
    initial_y = paddle.get_y()
    
    # Try to move up
    paddle.move(up=True)
    
    # Should not move past boundary
    assert paddle.get_y() == initial_y


def test_paddle_bottom_boundary(paddle: Paddle) -> None:
    """Test paddle stops at bottom boundary."""
    # Move paddle to bottom boundary
    max_y = GAME_AREA_TOP + GAME_AREA_HEIGHT - PADDLE_HEIGHT
    paddle.set_y(max_y)
    initial_y = paddle.get_y()
    
    # Try to move down
    paddle.move(up=False)
    
    # Should not move past boundary
    assert paddle.get_y() == initial_y 