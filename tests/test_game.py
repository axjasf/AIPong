"""Test suite for game state and scoring."""

import pytest
import pygame
from src.game import Game
from src.constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    GAME_AREA_WIDTH,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    BALL_SIZE
)


@pytest.fixture
def game():
    """Create a game fixture for tests."""
    pygame.init()
    return Game()


def test_game_initialization(game):
    """Test game is initialized with correct state."""
    assert game.player1.score == 0
    assert game.player2.score == 0
    assert not game.game_over
    assert game.ball is not None
    assert game.player1.paddle is not None
    assert game.player2.paddle is not None


def test_game_scoring_p1(game):
    """Test player 1 scoring."""
    initial_score = game.player1.score
    
    # Move ball past right boundary to trigger p1 score
    game.ball.x = GAME_AREA_WIDTH + BALL_SIZE
    game.update()
    
    assert game.player1.score == initial_score + 1
    assert game.ball.x == GAME_AREA_WIDTH // 2  # Ball should reset


def test_game_scoring_p2(game):
    """Test player 2 scoring."""
    initial_score = game.player2.score
    
    # Move ball past left boundary to trigger p2 score
    game.ball.x = -BALL_SIZE
    game.update()
    
    assert game.player2.score == initial_score + 1
    assert game.ball.x == GAME_AREA_WIDTH // 2  # Ball should reset


def test_game_over_condition(game):
    """Test game over condition."""
    # Set score close to winning
    game.player1.score = 9
    assert not game.game_over
    
    # Score winning point
    game.ball.x = GAME_AREA_WIDTH + BALL_SIZE
    game.update()
    
    assert game.game_over
    assert game.player1.score == 10


def test_paddle_movement(game):
    """Test paddle movement in game context."""
    initial_y_p1 = game.player1.paddle.get_y()
    initial_y_p2 = game.player2.paddle.get_y()
    
    # Move paddles through player objects
    game.player1.paddle.move(up=True)
    game.player2.paddle.move(up=False)
    
    assert game.player1.paddle.get_y() < initial_y_p1
    assert game.player2.paddle.get_y() > initial_y_p2


def test_ball_paddle_collision(game):
    """Test ball collision with paddles in game context."""
    # Position ball near p1 paddle
    game.ball.x = PADDLE_WIDTH + BALL_SIZE
    game.ball.y = game.player1.paddle.get_y() + (PADDLE_HEIGHT // 2)
    game.ball.angle = 180  # Moving left
    
    # Update ball rect for collision detection
    game.ball.rect.x = int(game.ball.x)
    game.ball.rect.y = int(game.ball.y)
    
    initial_angle = game.ball.angle
    game.update()
    
    # After collision, angle should be normalized to 0-360 range
    assert 0 <= game.ball.angle <= 360
    # Angle should change to roughly opposite direction (180 ± some randomness)
    assert 160 <= game.ball.angle <= 200 