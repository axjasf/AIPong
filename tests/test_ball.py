"""Test suite for ball movement and collisions."""

import pytest
import pygame
import math
from src.ball import Ball
from src.paddle import Paddle
from src.constants import (
    WINDOW_WIDTH,
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    BALL_SPEED,
    BALL_SIZE,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)


@pytest.fixture
def ball() -> Ball:
    """Create a ball fixture for tests."""
    pygame.init()
    return Ball()


@pytest.fixture
def paddle() -> Paddle:
    """Create a paddle fixture for tests."""
    pygame.init()
    x = 100
    y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2)
    return Paddle(x, y)


def test_ball_initialization(ball: Ball) -> None:
    """Test ball is initialized with correct position and properties."""
    assert ball.x == WINDOW_WIDTH / 2 - BALL_SIZE / 2
    assert ball.y == GAME_AREA_TOP + (GAME_AREA_HEIGHT / 2) - (BALL_SIZE / 2)
    assert ball.rect.width == BALL_SIZE
    assert ball.rect.height == BALL_SIZE
    assert ball.speed == BALL_SPEED
    assert abs(ball.dx) + abs(ball.dy) == pytest.approx(BALL_SPEED, rel=1e-5)


def test_ball_initial_direction() -> None:
    """Test that multiple balls start with different random directions."""
    directions = set()
    for _ in range(10):
        ball = Ball()
        direction = (ball.dx, ball.dy)
        directions.add(direction)
    # With 10 balls, we should get at least 3 different directions
    assert len(directions) >= 3


def test_ball_movement(ball: Ball) -> None:
    """Test ball moves correctly."""
    initial_x = ball.x
    initial_y = ball.y
    initial_dx = ball.dx
    initial_dy = ball.dy
    
    ball.move([])
    
    assert ball.x == initial_x + initial_dx
    assert ball.y == initial_y + initial_dy


def test_ball_reset(ball: Ball) -> None:
    """Test ball reset functionality."""
    # Move ball to some position
    ball.x = 100
    ball.y = 100
    initial_speed = ball.speed
    
    ball.reset()
    
    assert ball.x == WINDOW_WIDTH / 2 - BALL_SIZE / 2
    assert ball.y == GAME_AREA_TOP + (GAME_AREA_HEIGHT / 2) - (BALL_SIZE / 2)
    assert ball.speed == initial_speed
    assert abs(ball.dx) + abs(ball.dy) == pytest.approx(BALL_SPEED, rel=1e-5)


def test_ball_top_boundary(ball: Ball) -> None:
    """Test ball bounces off top boundary."""
    # Move ball to top boundary
    ball.y = GAME_AREA_TOP
    ball.dy = -abs(ball.dy)  # Ensure moving up
    initial_dy = ball.dy
    initial_dx = ball.dx
    
    ball.move([])
    
    assert ball.dy == abs(initial_dy)  # Should bounce down
    assert ball.dx == initial_dx  # Horizontal direction unchanged


def test_ball_bottom_boundary(ball: Ball) -> None:
    """Test ball bounces off bottom boundary."""
    # Move ball to bottom boundary
    ball.y = GAME_AREA_TOP + GAME_AREA_HEIGHT - BALL_SIZE
    ball.dy = abs(ball.dy)  # Ensure moving down
    initial_dy = ball.dy
    initial_dx = ball.dx
    
    ball.move([])
    
    assert ball.dy == -abs(initial_dy)  # Should bounce up
    assert ball.dx == initial_dx  # Horizontal direction unchanged


def test_ball_paddle_collision(ball: Ball, paddle: Paddle) -> None:
    """Test ball bounces off paddle."""
    # Test collision with left paddle
    paddle.is_left = True
    ball.x = paddle.x + paddle.width - 1  # Position ball just before collision
    ball.y = paddle.y + (PADDLE_HEIGHT // 2)
    initial_speed = ball.speed
    ball.dx = -abs(ball.dx)  # Ensure moving left
    
    # Update ball rect for collision detection
    ball.rect.x = int(ball.x)
    ball.rect.y = int(ball.y)
    
    # Move ball to collide with paddle
    ball.move([paddle])
    
    # Ball should have bounced off paddle
    assert ball.dx > 0, "Ball should be moving right after collision with left paddle"
    assert ball.speed > initial_speed, "Speed should increase after collision"
    
    # Test collision with right paddle
    paddle.is_left = False
    ball.x = paddle.x - ball.size + 1  # Position ball just before collision
    ball.y = paddle.y + (PADDLE_HEIGHT // 2)
    initial_speed = ball.speed
    ball.dx = abs(ball.dx)  # Ensure moving right
    
    # Update ball rect for collision detection
    ball.rect.x = int(ball.x)
    ball.rect.y = int(ball.y)
    
    # Move ball to collide with paddle
    ball.move([paddle])
    
    # Ball should have bounced off paddle
    assert ball.dx < 0, "Ball should be moving left after collision with right paddle"
    assert ball.speed > initial_speed, "Speed should increase after collision"


def test_ball_paddle_collision_angle(ball: Ball, paddle: Paddle) -> None:
    """Test ball-paddle collision affects vertical direction based on hit position."""
    # Test hitting different parts of the paddle
    positions = [
        (0.2, True),  # Hit near top - should go up
        (0.8, False),  # Hit near bottom - should go down
        (0.5, None),  # Hit middle - could go either way
    ]
    
    for relative_pos, should_go_up in positions:
        # Position ball just to the left of paddle
        ball.x = paddle.x - BALL_SIZE
        ball.y = paddle.y + (PADDLE_HEIGHT * relative_pos)
        ball.dx = abs(ball.dx)  # Ensure moving right
        
        # Update ball rect for collision detection
        ball.rect.x = int(ball.x)
        ball.rect.y = int(ball.y)
        
        ball.move([paddle])
        
        if should_go_up is True:
            assert ball.dy < 0, "Ball should move upward after hitting top of paddle"
        elif should_go_up is False:
            assert ball.dy > 0, "Ball should move downward after hitting bottom of paddle" 