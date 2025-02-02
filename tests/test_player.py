"""Test suite for player classes."""

import pytest
import pygame
from src.player import HumanPlayer, ComputerPlayer, AIPlayer
from src.paddle import Paddle
from src.ball import Ball
from src.constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    BALL_SIZE,
    P1_UP_KEY,
    P1_DOWN_KEY,
)


@pytest.fixture
def paddle() -> Paddle:
    """Create a paddle fixture for tests."""
    return Paddle(0, GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2, True)


@pytest.fixture
def ball() -> Ball:
    """Create a ball fixture for tests."""
    return Ball()


def test_human_player_initialization(paddle: Paddle) -> None:
    """Test human player initialization."""
    player = HumanPlayer(paddle, P1_UP_KEY, P1_DOWN_KEY)
    assert player.paddle == paddle
    assert player.score == 0
    assert player.up_key == P1_UP_KEY
    assert player.down_key == P1_DOWN_KEY


def test_computer_player_initialization(paddle: Paddle) -> None:
    """Test computer player initialization."""
    player = ComputerPlayer(paddle)
    assert player.paddle == paddle
    assert player.score == 0
    assert player.ball is None
    assert player.last_ball_y == 0.0


def test_computer_player_no_movement_without_ball(paddle: Paddle) -> None:
    """Test computer player doesn't move without ball reference."""
    player = ComputerPlayer(paddle)
    initial_y = player.paddle.get_y()

    player.update()
    assert player.paddle.get_y() == initial_y


def test_computer_player_follows_ball_up(paddle: Paddle, ball: Ball) -> None:
    """Test computer player follows ball moving up."""
    player = ComputerPlayer(paddle)
    player.ball = ball

    # Position ball above paddle
    initial_paddle_y = paddle.get_y()
    ball_y = initial_paddle_y - BALL_SIZE * 2
    player.ball.y = ball_y

    player.update()
    assert player.paddle.get_y() < initial_paddle_y  # Paddle should move up


def test_computer_player_follows_ball_down(paddle: Paddle, ball: Ball) -> None:
    """Test computer player follows ball moving down."""
    player = ComputerPlayer(paddle)
    player.ball = ball

    # Position ball below paddle
    initial_paddle_y = paddle.get_y()
    ball_y = initial_paddle_y + PADDLE_HEIGHT + BALL_SIZE
    player.ball.y = ball_y

    player.update()
    assert player.paddle.get_y() > initial_paddle_y  # Paddle should move down


def test_computer_player_stays_in_bounds_top(paddle: Paddle, ball: Ball) -> None:
    """Test computer player doesn't move above game area."""
    player = ComputerPlayer(paddle)
    player.ball = ball

    # Position paddle at top
    paddle.set_y(GAME_AREA_TOP)
    # Position ball above paddle
    player.ball.y = GAME_AREA_TOP - BALL_SIZE

    player.update()
    assert player.paddle.get_y() == GAME_AREA_TOP  # Should stay at top


def test_computer_player_stays_in_bounds_bottom(paddle: Paddle, ball: Ball) -> None:
    """Test computer player doesn't move below game area."""
    player = ComputerPlayer(paddle)
    player.ball = ball

    # Position paddle at bottom
    bottom_y = GAME_AREA_TOP + GAME_AREA_HEIGHT - PADDLE_HEIGHT
    paddle.set_y(bottom_y)
    # Position ball below paddle
    player.ball.y = GAME_AREA_TOP + GAME_AREA_HEIGHT

    player.update()
    assert player.paddle.get_y() == bottom_y  # Should stay at bottom


def test_computer_player_deadzone(paddle: Paddle, ball: Ball) -> None:
    """Test computer player deadzone behavior."""
    player = ComputerPlayer(paddle)
    player.ball = ball

    # Position ball slightly above paddle center (within deadzone)
    initial_paddle_y = paddle.get_y()
    paddle_center = initial_paddle_y + (PADDLE_HEIGHT / 2)
    ball_y = paddle_center - 5  # Within 10-pixel deadzone
    player.ball.y = ball_y

    player.update()
    assert player.paddle.get_y() == initial_paddle_y  # Should not move


def test_player_score_management(paddle: Paddle) -> None:
    """Test player score management."""
    player = ComputerPlayer(paddle)  # Could use any player type

    assert player.score == 0
    player.increment_score()
    assert player.score == 1
    player.reset_score()
    assert player.score == 0
