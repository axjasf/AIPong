"""Test suite for ball movement and collisions."""

import pytest
import pygame
import math
from src.ball import Ball
from src.paddle import Paddle
from src.constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    GAME_AREA_WIDTH,
    BALL_SPEED,
    BALL_SIZE,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)


@pytest.fixture
def ball():
    """Create a ball fixture for tests."""
    pygame.init()
    x = GAME_AREA_WIDTH // 2
    y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2)
    return Ball(x, y)


@pytest.fixture
def paddle():
    """Create a paddle fixture for tests."""
    pygame.init()
    x = 100
    y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2)
    return Paddle(x, y, GAME_AREA_TOP, GAME_AREA_TOP + GAME_AREA_HEIGHT)


def test_ball_initialization(ball):
    """Test ball is initialized with correct position and properties."""
    assert ball.x == GAME_AREA_WIDTH // 2
    assert ball.y == float(GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2))
    assert ball.rect.width == BALL_SIZE
    assert ball.rect.height == BALL_SIZE
    assert ball.velocity == BALL_SPEED


def test_ball_movement(ball):
    """Test ball moves correctly."""
    initial_x = ball.x
    initial_y = ball.y
    rad_angle = math.radians(ball.angle)
    dx = ball.velocity * math.cos(rad_angle)
    dy = ball.velocity * math.sin(rad_angle)
    
    ball.move([])
    
    assert abs(ball.x - (initial_x + dx)) < 0.0001  # Allow for floating point imprecision
    assert abs(ball.y - (initial_y + dy)) < 0.0001


def test_ball_top_boundary(ball):
    """Test ball bounces off top boundary."""
    # Move ball to top boundary
    ball.y = GAME_AREA_TOP
    ball.angle = 315  # Moving up-left
    initial_angle = ball.angle
    
    ball.move([])
    
    assert ball.angle == -initial_angle  # Direction should reverse


def test_ball_bottom_boundary(ball):
    """Test ball bounces off bottom boundary."""
    # Move ball to bottom boundary
    ball.y = GAME_AREA_TOP + GAME_AREA_HEIGHT - BALL_SIZE
    ball.angle = 45  # Moving down-right
    initial_angle = ball.angle
    
    ball.move([])
    
    assert ball.angle == -initial_angle  # Direction should reverse


def test_ball_paddle_collision(ball, paddle):
    """Test ball bounces off paddle."""
    # Position ball just to the left of paddle
    ball.x = paddle.x - BALL_SIZE
    ball.y = paddle.y + (PADDLE_HEIGHT // 2)
    ball.angle = 0  # Moving right towards paddle
    
    # Update ball rect for collision detection
    ball.rect.x = int(ball.x)
    ball.rect.y = int(ball.y)
    
    # Move ball until it collides with paddle
    collision_detected = False
    for _ in range(10):  # Try a few times
        if ball.rect.colliderect(paddle.rect):
            collision_detected = True
            break
        ball.move([paddle])
    
    assert collision_detected, "Ball should have collided with paddle"
    
    # After collision, angle should be normalized to 0-360 range
    assert 0 <= ball.angle <= 360
    # Angle should change to roughly opposite direction (180 ± some randomness)
    assert 160 <= ball.angle <= 200 