"""Test suite for game UI."""

import pytest
import pygame
from unittest.mock import MagicMock, patch
from src.game_ui import GameUI
from src.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    SCORE_COLOR,
    SCORE_FONT_SIZE,
    WINNER_FONT_SIZE,
)


@pytest.fixture
def game_ui():
    """Fixture for game UI instance."""
    pygame.init()
    screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    ui = GameUI(screen)
    yield ui
    pygame.quit()


def test_game_ui_initialization(game_ui):
    """Test game UI initialization."""
    assert game_ui.screen is not None
    assert game_ui.score_font is not None
    assert game_ui.winner_font is not None
    assert not game_ui.headless


@patch('pygame.font.Font.render')
def test_draw_scores(mock_render, game_ui):
    """Test score rendering."""
    # Mock the font render function
    mock_surface = MagicMock()
    mock_surface.get_rect.return_value = pygame.Rect(0, 0, 50, 20)
    mock_render.return_value = mock_surface
    
    # Test score drawing
    game_ui.draw_scores(5, 3)
    
    # Verify both scores were rendered
    mock_render.assert_any_call("5", True, SCORE_COLOR)
    mock_render.assert_any_call("3", True, SCORE_COLOR)


@patch('pygame.font.Font.render')
def test_draw_winner(mock_render, game_ui):
    """Test winner message rendering."""
    mock_surface = MagicMock()
    mock_surface.get_rect.return_value = pygame.Rect(0, 0, 150, 30)
    mock_render.return_value = mock_surface
    
    # Test winner message
    game_ui.draw_winner("Player 1")
    mock_render.assert_called_with(
        "Player 1 Wins! Press SPACE for new game",
        True,
        (255, 255, 255)  # White
    )


def test_screen_update(game_ui):
    """Test screen update integration."""
    # Create a test surface
    test_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    game_ui.screen = test_surface
    
    # Get initial pixel at score position
    initial_pixel = test_surface.get_at((WINDOW_WIDTH // 2, 30))
    
    # Draw scores
    game_ui.draw_scores(1, 1)
    
    # Get pixel after rendering
    final_pixel = test_surface.get_at((WINDOW_WIDTH // 2, 30))
    
    # Pixels should be different after rendering
    assert initial_pixel != final_pixel 