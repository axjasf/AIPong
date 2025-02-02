"""Test suite for game logic."""

import pytest
import pygame
from src.game import Game
from src.constants import (
    WINDOW_WIDTH,
    GAME_AREA_WIDTH,
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    POINTS_TO_WIN,
    PADDLE_HEIGHT,
    BALL_SIZE,
)


@pytest.fixture
def game() -> Game:
    """Create a game fixture for tests."""
    pygame.init()
    return Game()


def test_game_initialization(game: Game) -> None:
    """Test game is initialized with correct state."""
    assert game.running
    assert not game.game_over
    assert game.winner is None
    assert game.player1.score == 0
    assert game.player2.score == 0


def test_game_scoring_p1(game: Game) -> None:
    """Test player 1 scoring."""
    # Move ball to right edge to trigger score
    game.ball.x = WINDOW_WIDTH - 1
    game.ball.dx = 1  # Moving right
    
    # Update game to trigger scoring
    game.update()
    
    assert game.player1.score == 1
    assert game.player2.score == 0
    # Ball should be at the right edge
    assert game.ball.x == WINDOW_WIDTH - BALL_SIZE


def test_game_scoring_p2(game: Game) -> None:
    """Test player 2 scoring."""
    # Move ball to left edge to trigger score
    game.ball.x = 1
    game.ball.dx = -1  # Moving left
    
    # Update game to trigger scoring
    game.update()
    
    assert game.player1.score == 0
    assert game.player2.score == 1
    # Ball should be at the left edge
    assert game.ball.x == 0


def test_game_over_condition(game: Game) -> None:
    """Test game over condition."""
    # Give player 1 winning score
    game.player1.score = POINTS_TO_WIN
    
    # Update game to trigger game over check
    game.ball.x = WINDOW_WIDTH - 1  # Position for scoring
    game.ball.dx = 1  # Moving right
    game.update()
    
    assert game.game_over
    assert game.winner == "Player 1"


def test_paddle_movement(game: Game) -> None:
    """Test paddle movement."""
    initial_y = game.player1.paddle.y
    
    # Move paddle up
    game.player1.paddle.move_up()
    assert game.player1.paddle.y == initial_y - game.player1.paddle.speed
    
    # Move paddle down
    game.player1.paddle.move_down()
    assert game.player1.paddle.y == initial_y


def test_ball_paddle_collision(game: Game) -> None:
    """Test ball-paddle collision."""
    # Position ball just to the left of paddle 1
    game.ball.x = game.player1.paddle.x + game.player1.paddle.width
    game.ball.y = game.player1.paddle.y + (PADDLE_HEIGHT // 2)
    game.ball.dx = -1  # Moving left
    
    # Update game to trigger collision
    game.update()
    
    # Ball should bounce right
    assert game.ball.dx > 0 