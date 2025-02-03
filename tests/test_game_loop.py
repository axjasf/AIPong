"""Test suite for game loop."""

import pytest
import pygame
from unittest.mock import MagicMock, patch
from src.game_loop import GameLoop
from src.game import Game
from src.constants import (
    FPS,
    WINDOW_WIDTH,
    PADDLE_WIDTH,
    BALL_SIZE,
    POINTS_TO_WIN,
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_HEIGHT,
)
from src.ball import Ball
from src.player import HumanPlayer
from src.game_state import GameState
from src.game_score import GameScore
from src.paddle import Paddle


@pytest.fixture
def game_loop():
    """Fixture for game loop instance."""
    pygame.init()
    
    # Create required components
    ball = Ball()
    paddle1 = Paddle(50, 300, True)  # Left paddle
    paddle2 = Paddle(750, 300, False)  # Right paddle
    player1 = HumanPlayer(paddle1, pygame.K_w, pygame.K_s)
    player2 = HumanPlayer(paddle2, pygame.K_UP, pygame.K_DOWN)
    game_state = GameState()
    scoring = GameScore()
    
    # Create game loop with all required components
    loop = GameLoop(
        ball=ball,
        player1=player1,
        player2=player2,
        game_state=game_state,
        scoring=scoring,
        headless=True  # Use headless mode for testing
    )
    
    yield loop
    pygame.quit()


def test_game_loop_initialization(game_loop):
    """Test game loop initialization."""
    assert game_loop.clock is not None
    assert game_loop.running
    assert not game_loop.game_over
    assert not game_loop.waiting_for_reset


@patch('pygame.event.get')
def test_handle_input_quit(mock_event_get, game_loop):
    """Test handling quit event."""
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT
    mock_event_get.return_value = [mock_event]
    
    game_loop.headless = False  # Disable headless mode for this test
    game_loop.handle_input()
    assert not game_loop.running


@patch('pygame.event.get')
def test_handle_input_reset(mock_event_get, game_loop):
    """Test handling reset event."""
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_SPACE
    mock_event_get.return_value = [mock_event]
    
    # Setup game state
    game_loop.headless = False  # Disable headless mode for this test
    game_loop.game_over = True
    game_loop.winner = "Player 1"
    game_loop.player1.increment_score()
    
    # Trigger reset
    game_loop.handle_input()
    
    # Verify reset occurred
    assert not game_loop.game_over
    assert game_loop.winner is None
    assert game_loop.player1.score == 0


def test_update(game_loop):
    """Test game loop update."""
    # Test update when not in reset state
    initial_ball_x = game_loop.ball.x
    game_loop.update()
    assert game_loop.ball.x != initial_ball_x  # Ball should move
    
    # Test update during reset
    game_loop.waiting_for_reset = True
    game_loop.headless = True  # Skip delay in test
    ball_x_before_reset = game_loop.ball.x
    game_loop.update()
    assert game_loop.ball.x != ball_x_before_reset  # Ball should be reset
    assert not game_loop.waiting_for_reset  # Reset should be complete


def test_draw(game_loop):
    """Test game loop draw."""
    # Test that draw doesn't fail in headless mode
    game_loop.draw()
    assert True  # If we get here, no exception was raised


def test_reset_game(game_loop):
    """Test game reset functionality."""
    # Modify game state
    game_loop.player1.increment_score()
    game_loop.player2.increment_score()
    initial_velocity = (game_loop.ball.dx, game_loop.ball.dy)
    
    # Reset game
    game_loop.reset_game()
    
    # Verify reset state
    assert game_loop.player1.score == 0
    assert game_loop.player2.score == 0
    # Ball should be in center but with new velocity
    current_velocity = (game_loop.ball.dx, game_loop.ball.dy)
    assert current_velocity != initial_velocity, f"Ball velocity should change after reset. Was {initial_velocity}, still {current_velocity}"
    assert not game_loop.game_over
    assert game_loop.winner is None


def test_run_integration(game_loop):
    """Test basic game loop integration."""
    # Set up initial state
    initial_score = game_loop.player1.score
    
    # Force a win condition by scoring enough points
    for _ in range(POINTS_TO_WIN):
        game_loop.player1.increment_score()
        game_loop.scoring.increment_score(True)
    
    # Set game over state since we've reached win condition
    game_loop.game_over = True
    game_loop.winner = "Player 1"
    
    # Verify game is in winning state before running
    assert game_loop.scoring.check_winner() == 0  # Player 1 should be winner
    print("Game state before run: game_over={}, winner={}, games_completed={}".format(
        game_loop.game_over, game_loop.winner, game_loop.games_completed))
    
    # Run for exactly one game (will end when someone wins)
    game_loop.run(max_games=10)  # Use 10 games to avoid milestone division issues
    
    print("Game state after run: game_over={}, winner={}, games_completed={}".format(
        game_loop.game_over, game_loop.winner, game_loop.games_completed))
    
    # Verify game completed properly
    assert game_loop.games_completed == 1  # Should complete one game
    assert not game_loop.running  # Should stop running
    assert game_loop.player1.score == 0  # Score should be reset
    assert game_loop.player2.score == 0  # Score should be reset 