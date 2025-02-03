"""Test suite for game class."""

import pytest
import pygame
from src.game import Game
from src.player import HumanPlayer, ComputerPlayer
from src.constants import (
    WINDOW_WIDTH,
    PADDLE_WIDTH,
    BALL_SIZE,
    POINTS_TO_WIN,
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_HEIGHT,
)
import logging


@pytest.fixture
def game():
    """Fixture for game instance."""
    pygame.init()
    game = Game()
    yield game
    pygame.quit()


def test_game_initialization(game):
    """Test game initialization."""
    # Test player initialization
    assert isinstance(game.player1, HumanPlayer)
    assert isinstance(game.player2, HumanPlayer)
    
    # Test game objects initialization
    assert game.ball is not None
    assert len(game.paddles) == 2
    assert game.game_state is not None
    
    # Test initial game state
    assert game.running
    assert not game.game_over
    assert not game.waiting_for_reset
    assert not game.is_paused


def test_game_reset(game):
    """Test game reset functionality."""
    # Modify game state
    game.player1.increment_score()
    game.player2.increment_score()
    initial_ball_pos = (game.ball.x, game.ball.y)
    initial_ball_vel = (game.ball.dx, game.ball.dy)
    
    # Move paddles
    initial_p1_y = game.paddles[0].get_y()
    initial_p2_y = game.paddles[1].get_y()
    game.paddles[0].move_up()
    game.paddles[1].move_down()
    
    # Reset game
    game.reset_game()
    
    # Verify reset state
    assert game.score == (0, 0)  # Scores should reset to 0-0
    # Ball should be back at center (same position)
    assert (game.ball.x, game.ball.y) == initial_ball_pos
    # Ball velocity should be randomized (different direction)
    assert (game.ball.dx, game.ball.dy) != initial_ball_vel
    assert game.paddles[0].get_y() == initial_p1_y
    assert game.paddles[1].get_y() == initial_p2_y


def test_game_pause_toggle(game):
    """Test game pause functionality."""
    assert not game.is_paused
    game.toggle_pause()
    assert game.is_paused
    game.toggle_pause()
    assert not game.is_paused


def test_ball_paddle_collision(game):
    """Test ball collision with paddles."""
    # Position ball near left paddle's right edge
    game.ball.x = game.paddles[0].rect.right - BALL_SIZE // 2  # Position ball overlapping with paddle
    game.ball.y = game.paddles[0].get_y() + PADDLE_HEIGHT // 2
    game.ball.speed = 2.0  # Set a slower speed
    game.ball.dx = -game.ball.speed  # Move left at full speed
    game.ball.dy = 0  # No vertical movement to simplify test
    
    # Update ball's rect to match new position
    game.ball.rect.x = int(game.ball.x)
    game.ball.rect.y = int(game.ball.y)
    
    # Store initial speed for comparison
    initial_speed = game.ball.speed
    
    # Update game
    game.update()
    
    # Ball should bounce off paddle (direction should reverse)
    assert game.ball.dx > 0, "Ball should change direction after hitting paddle"
    assert game.ball.speed > initial_speed, "Ball should increase speed after collision"
    assert game.ball.x >= game.paddles[0].rect.right, "Ball should be past the paddle's right edge"


def test_ball_wall_collision(game):
    """Test ball collision with walls."""
    # Position ball near top wall
    game.ball.y = GAME_AREA_TOP + 1  # Position ball just above top wall
    game.ball.dy = -2.0  # Set a fixed upward velocity
    game.ball.dx = 2.0  # Set a fixed horizontal velocity
    
    # Update ball's rect to match new position
    game.ball.rect.x = int(game.ball.x)
    game.ball.rect.y = int(game.ball.y)
    
    # Store initial values
    initial_dy = game.ball.dy
    
    # Update game
    game.update()
    
    # Ball should bounce off wall
    assert game.ball.dy > 0, "Ball should change vertical direction after hitting wall"
    assert abs(game.ball.dy) == abs(initial_dy), "Ball should maintain speed after wall collision"
    assert game.ball.dx == 2.0, "Horizontal velocity should not change"
    assert game.ball.y >= GAME_AREA_TOP, "Ball should not go beyond game area"


def test_scoring(game):
    """Test scoring system."""
    # Move ball past right paddle
    initial_score = game.score[0]  # Left player score
    game.ball.x = WINDOW_WIDTH + BALL_SIZE
    game.headless = True  # Enable headless mode to skip reset delay
    
    # Update ball's rect to match new position
    game.ball.rect.x = int(game.ball.x)
    game.ball.rect.y = int(game.ball.y)
    
    # Update game to trigger scoring
    game.update()
    
    # Left player should score
    assert game.score[0] == initial_score + 1, "Score should increment"
    assert game.waiting_for_reset, "Game should be waiting to reset ball"
    
    # Update again to perform the reset
    game.update()
    
    # Ball should be at center
    center_x = WINDOW_WIDTH / 2 - game.ball.size / 2
    center_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT / 2) - (game.ball.size / 2)
    assert game.ball.x == center_x, "Ball should be centered horizontally"
    assert game.ball.y == center_y, "Ball should be centered vertically"
    assert not game.waiting_for_reset, "Reset should be complete"


def test_player_movement(game):
    """Test player movement."""
    # Get initial paddle positions
    initial_left_y = game.paddles[0].get_y()
    initial_right_y = game.paddles[1].get_y()
    
    # Simulate left player moving up
    keys = [0] * 512  # pygame.K_LAST
    keys[pygame.K_w] = 1
    pygame.event.get = lambda: []  # Mock event queue
    pygame.key.get_pressed = lambda: keys
    
    # Update game
    game.update()
    
    # Left paddle should move up
    assert game.paddles[0].get_y() < initial_left_y
    
    # Right paddle position may change based on AI/computer behavior
    assert game.paddles[1].get_y() != initial_right_y


def test_game_over_condition(game):
    """Test game over condition."""
    # Score enough points to trigger game over
    for _ in range(POINTS_TO_WIN):
        game.player1.increment_score()
    
    # Update game
    game.update()
    
    # Game should be over
    assert game.game_over
    assert game.winner == "Player 1"


def test_point_scored_reset(game):
    """Test reset behavior when a point is scored (during game)."""
    # Enable headless mode for immediate reset
    game.headless = True
    
    # Score a point
    initial_score = game.score[0]  # Left player score
    game.ball.x = WINDOW_WIDTH + BALL_SIZE  # Move ball past right paddle
    
    # Remember positions
    initial_ball_pos = (game.ball.x, game.ball.y)
    initial_ball_vel = (game.ball.dx, game.ball.dy)
    
    # Update should trigger point scoring
    game.update()
    
    # Score should increase but game should continue
    assert game.score[0] == initial_score + 1
    assert not game.game_over
    assert game.waiting_for_reset  # Ball reset is pending
    
    # Update again to perform the reset
    game.update()
    
    # Ball should be back at center with new direction
    center_x = WINDOW_WIDTH / 2 - game.ball.size / 2
    center_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT / 2) - (game.ball.size / 2)
    assert (game.ball.x, game.ball.y) == (center_x, center_y)  # Exactly at center
    assert (game.ball.dx, game.ball.dy) != initial_ball_vel  # New direction
    
    # Paddles should be back at center height
    paddle_center_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2
    assert game.paddles[0].get_y() == paddle_center_y
    assert game.paddles[1].get_y() == paddle_center_y 