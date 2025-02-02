"""Test suite for player classes."""

import pytest
import pygame
from src.player import HumanPlayer, ComputerPlayer
from src.paddle import Paddle
from src.ball import Ball
from src.constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
)


@pytest.fixture
def paddle():
    """Fixture for paddle."""
    return Paddle(0, GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2, True)


@pytest.fixture
def ball():
    """Fixture for ball."""
    return Ball()


def test_human_player_initialization(paddle):
    """Test human player initialization."""
    up_key = pygame.K_w
    down_key = pygame.K_s
    player = HumanPlayer(paddle, up_key, down_key)
    
    assert player.paddle == paddle
    assert player.score == 0
    assert player.up_key == up_key
    assert player.down_key == down_key


def test_computer_player_initialization(paddle):
    """Test computer player initialization."""
    player = ComputerPlayer(paddle)
    assert player.paddle == paddle
    assert player.score == 0
    assert player.ball is None
    assert player.last_ball_y == 0.0


def test_computer_player_no_movement_without_ball(paddle):
    """Test computer player doesn't move without ball reference."""
    player = ComputerPlayer(paddle)
    initial_y = player.paddle.get_y()
    
    player.update()
    assert player.paddle.get_y() == initial_y


def test_computer_player_follows_ball(paddle, ball, monkeypatch):
    """Test computer player follows the ball's vertical movement."""
    # Initialize with hard difficulty for minimal delay
    player = ComputerPlayer(paddle, difficulty="hard")
    player.ball = ball
    player.last_update_time = 0  # Reset last update time
    
    # Position paddle in middle of game area
    middle_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2
    paddle.set_y(middle_y)
    
    # Mock pygame time to ensure movement
    time_ms = 0
    def mock_get_ticks():
        nonlocal time_ms
        time_ms += 250  # Increment by more than any possible reaction delay
        return time_ms
    monkeypatch.setattr(pygame.time, "get_ticks", mock_get_ticks)
    
    # Test upward movement - place ball well above paddle and outside deadzone
    ball.y = middle_y - PADDLE_HEIGHT * 2  # Place ball above paddle
    start_y = paddle.get_y()
    current_y = start_y
    
    # Update multiple times to ensure movement
    moved = False
    for _ in range(10):  # More updates to ensure movement
        player.update()
        # Verify movement after each update
        current_y = paddle.get_y()
        if current_y < start_y:
            moved = True
            break  # Movement detected
    assert moved, f"Paddle should move up from {start_y} but stayed at {current_y}"
    
    # Reset and test downward movement
    paddle.set_y(middle_y)
    ball.y = middle_y + PADDLE_HEIGHT * 2  # Place ball below paddle
    start_y = paddle.get_y()
    current_y = start_y
    player.last_update_time = 0  # Reset last update time
    
    # Update multiple times to ensure movement
    moved = False
    for _ in range(10):  # More updates to ensure movement
        player.update()
        # Verify movement after each update
        current_y = paddle.get_y()
        if current_y > start_y:
            moved = True
            break  # Movement detected
    assert moved, f"Paddle should move down from {start_y} but stayed at {current_y}"


def test_computer_player_stays_in_bounds(paddle, ball):
    """Test computer player stays within game boundaries."""
    player = ComputerPlayer(paddle)
    player.ball = ball
    
    # Test upper boundary
    paddle.set_y(GAME_AREA_TOP)
    ball.y = GAME_AREA_TOP - PADDLE_HEIGHT
    player.update()
    assert player.paddle.get_y() >= GAME_AREA_TOP
    
    # Test lower boundary
    paddle.set_y(GAME_AREA_TOP + GAME_AREA_HEIGHT - PADDLE_HEIGHT)
    ball.y = GAME_AREA_TOP + GAME_AREA_HEIGHT
    player.update()
    assert player.paddle.get_y() <= GAME_AREA_TOP + GAME_AREA_HEIGHT - PADDLE_HEIGHT


def test_computer_player_deadzone(paddle, ball):
    """Test computer player deadzone behavior."""
    player = ComputerPlayer(paddle)
    player.ball = ball
    initial_y = paddle.get_y()
    
    # Position ball slightly above paddle center (within deadzone)
    paddle_center = initial_y + (PADDLE_HEIGHT / 2)
    ball.y = paddle_center - (player.MOVEMENT_DEADZONE / 2)
    
    player.update()
    assert player.paddle.get_y() == initial_y  # Should not move


def test_player_score_management(paddle):
    """Test player score management."""
    player = ComputerPlayer(paddle)  # Could use any player type
    
    assert player.score == 0
    player.increment_score()
    assert player.score == 1
    player.reset_score()
    assert player.score == 0


def test_human_player_movement(paddle, monkeypatch):
    """Test human player movement with key presses."""
    player = HumanPlayer(paddle, pygame.K_w, pygame.K_s)
    
    # Position paddle in middle of game area to allow movement in both directions
    middle_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2
    paddle.set_y(middle_y)
    
    # Test upward movement
    start_y = paddle.get_y()
    current_y = start_y
    keys = [0] * 512  # pygame.K_LAST
    keys[pygame.K_w] = 1
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: keys)
    
    # Update multiple times to ensure visible movement
    moved = False
    for _ in range(3):
        player.update()
        # Verify movement after each update
        current_y = paddle.get_y()
        if current_y < start_y:
            moved = True
            break  # Movement detected
    assert moved, f"Paddle should move up from {start_y} but stayed at {current_y}"
    
    # Reset and test downward movement
    paddle.set_y(middle_y)
    start_y = paddle.get_y()
    current_y = start_y
    keys = [0] * 512
    keys[pygame.K_s] = 1
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: keys)
    
    # Update multiple times to ensure visible movement
    moved = False
    for _ in range(3):
        player.update()
        # Verify movement after each update
        current_y = paddle.get_y()
        if current_y > start_y:
            moved = True
            break  # Movement detected
    assert moved, f"Paddle should move down from {start_y} but stayed at {current_y}"
