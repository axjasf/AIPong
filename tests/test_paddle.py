"""Test suite for paddle movement and behavior."""

import pytest
import pygame
from src.paddle import Paddle
from src.constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_SPEED,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)


@pytest.fixture
def paddle() -> Paddle:
    """Create a paddle fixture for tests."""
    pygame.init()
    x = 100
    y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2)
    return Paddle(x, y)


def test_paddle_initialization(paddle: Paddle) -> None:
    """Test paddle is initialized with correct position and properties."""
    assert paddle.x == 100
    assert paddle.y == GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2)
    assert paddle.rect.width == PADDLE_WIDTH
    assert paddle.rect.height == PADDLE_HEIGHT
    assert paddle.speed == PADDLE_SPEED


def test_paddle_move_up(paddle: Paddle) -> None:
    """Test paddle moves up correctly."""
    initial_y = paddle.y
    paddle.move_up()
    assert paddle.y == initial_y - PADDLE_SPEED
    assert paddle.rect.y == int(paddle.y)  # Rectangle should update with position


def test_paddle_move_down(paddle: Paddle) -> None:
    """Test paddle moves down correctly."""
    initial_y = paddle.y
    paddle.move_down()
    assert paddle.y == initial_y + PADDLE_SPEED
    assert paddle.rect.y == int(paddle.y)  # Rectangle should update with position


def test_paddle_top_boundary(paddle: Paddle) -> None:
    """Test paddle stops at top boundary."""
    # Move paddle to top boundary
    paddle.y = GAME_AREA_TOP
    initial_y = paddle.y
    paddle.move_up()
    assert paddle.y == initial_y  # Should not move past top
    assert paddle.rect.y == int(paddle.y)


def test_paddle_bottom_boundary(paddle: Paddle) -> None:
    """Test paddle stops at bottom boundary."""
    # Move paddle to bottom boundary
    paddle.y = GAME_AREA_TOP + GAME_AREA_HEIGHT - PADDLE_HEIGHT
    initial_y = paddle.y
    paddle.move_down()
    assert paddle.y == initial_y  # Should not move past bottom
    assert paddle.rect.y == int(paddle.y)


def test_paddle_continuous_movement(paddle: Paddle) -> None:
    """Test paddle can move continuously within boundaries."""
    initial_y = paddle.y
    
    # Move up several times
    for _ in range(5):
        paddle.move_up()
    assert paddle.y == initial_y - (PADDLE_SPEED * 5)
    
    # Move down several times
    for _ in range(10):
        paddle.move_down()
    assert paddle.y == initial_y + (PADDLE_SPEED * 5)


def test_paddle_ai_movement(paddle: Paddle) -> None:
    """Test AI paddle movement behavior."""
    initial_y = paddle.y
    
    # Test moving towards ball above paddle
    ball_y = paddle.y - 100  # Ball is above paddle
    paddle.update_ai(ball_y)
    assert paddle.y < initial_y  # Should move up
    
    # Reset position
    initial_y = paddle.y
    
    # Test moving towards ball below paddle
    ball_y = paddle.y + 100  # Ball is below paddle
    paddle.update_ai(ball_y)
    assert paddle.y > initial_y  # Should move down
    
    # Reset position
    initial_y = paddle.y
    
    # Test not moving when ball is at paddle center
    ball_y = paddle.y + (PADDLE_HEIGHT / 2)
    paddle.update_ai(ball_y)
    assert paddle.y == initial_y  # Should not move


def test_paddle_rect_updates(paddle: Paddle) -> None:
    """Test that paddle's rectangle updates correctly with position."""
    initial_rect_y = paddle.rect.y
    
    # Move paddle
    paddle.move_down()
    
    # Rectangle should update to match new position
    assert paddle.rect.y == int(paddle.y)
    assert paddle.rect.y != initial_rect_y 