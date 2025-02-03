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
    P1_SCORE_X,
    SCORE_MARGIN_TOP,
)


@pytest.fixture
def game_ui():
    """Fixture for game UI instance."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    ui = GameUI(headless=False)
    yield ui
    pygame.quit()


def test_game_ui_initialization(game_ui):
    """Test game UI initialization."""
    assert game_ui.screen is not None
    assert game_ui.score_font is not None
    assert game_ui.winner_font is not None
    assert not game_ui.headless


@patch('pygame.font.SysFont')
def test_draw_scores(mock_sysfont, game_ui):
    """Test score rendering."""
    # Create a real surface for the mock to return
    mock_font = MagicMock()
    text_surface = pygame.Surface((50, 20))
    text_surface.fill(SCORE_COLOR)
    mock_font.render.return_value = text_surface
    mock_sysfont.return_value = mock_font
    
    # Replace the real fonts with our mock
    game_ui.score_font = mock_font
    
    # Fill screen with black
    game_ui.screen.fill((0, 0, 0))
    pygame.display.flip()
    
    # Draw scores
    game_ui.draw_scores(5, 3)
    pygame.display.flip()
    
    # Verify both scores were rendered
    mock_font.render.assert_any_call("5", True, SCORE_COLOR)
    mock_font.render.assert_any_call("3", True, SCORE_COLOR)


@patch('pygame.font.SysFont')
def test_draw_winner(mock_sysfont, game_ui):
    """Test winner message rendering."""
    # Create a real surface for the mock to return
    mock_font = MagicMock()
    text_surface = pygame.Surface((150, 30))
    text_surface.fill((255, 255, 255))  # White
    mock_font.render.return_value = text_surface
    mock_sysfont.return_value = mock_font
    
    # Replace the real fonts with our mock
    game_ui.winner_font = mock_font
    
    # Fill screen with black
    game_ui.screen.fill((0, 0, 0))
    pygame.display.flip()
    
    # Draw winner message
    game_ui.draw_winner("Player 1")
    pygame.display.flip()
    
    # Verify the winner message was rendered
    mock_font.render.assert_called_with(
        "Player 1 Wins! Press SPACE for new game",
        True,
        (255, 255, 255)  # White
    )


def test_screen_update(game_ui):
    """Test screen update integration."""
    # Fill screen with black
    game_ui.screen.fill((0, 0, 0))
    pygame.display.flip()
    
    # Get initial pixel at score position (left score)
    score_x = P1_SCORE_X  # Use constant for left player score position
    score_y = SCORE_MARGIN_TOP + 10  # Add small offset to ensure we hit the text
    initial_pixel = game_ui.screen.get_at((score_x, score_y))
    
    # Draw scores
    game_ui.draw_scores(1, 1)
    pygame.display.flip()
    
    # Get pixel after rendering
    final_pixel = game_ui.screen.get_at((score_x, score_y))
    
    # Initial pixel should be black, final pixel should be score color
    assert initial_pixel[0:3] == (0, 0, 0)  # Black
    assert final_pixel[0:3] == SCORE_COLOR  # Score color 