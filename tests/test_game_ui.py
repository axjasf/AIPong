"""Test suite for game UI."""

import pytest
import pygame
from unittest.mock import MagicMock, patch
from src.game_ui import GameUI
from src.ball import Ball
from src.paddle import Paddle
from src.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GAME_AREA_TOP,
    WHITE,
    SCORE_COLOR,
    SCORE_FONT_SIZE,
    WINNER_FONT_SIZE,
    P1_SCORE_X,
    P2_SCORE_X,
    SCORE_MARGIN_TOP,
)


@pytest.fixture
def mock_screen():
    """Fixture for mock screen with tracking capabilities."""
    class MockScreen:
        def __init__(self):
            self.fill_color = None
            self.blit_calls = []
            self.draw_line_calls = []
        
        def fill(self, color):
            self.fill_color = color
        
        def blit(self, surface, position):
            self.blit_calls.append((surface, position))
        
        def get_at(self, pos):
            return (0, 0, 0, 255)  # Default black
            
    return MockScreen()


@pytest.fixture
def mock_pygame_setup(monkeypatch, mock_screen):
    """Setup pygame mocks for testing."""
    class MockDisplay:
        @staticmethod
        def set_mode(size):
            return mock_screen
            
        @staticmethod
        def flip():
            pass
    
    class MockDraw:
        @staticmethod
        def line(surface, color, start_pos, end_pos):
            surface.draw_line_calls.append((color, start_pos, end_pos))
    
    monkeypatch.setattr(pygame, 'display', MockDisplay)
    monkeypatch.setattr(pygame, 'draw', MockDraw)
    return mock_screen


def test_headless_initialization():
    """Test game UI initialization in headless mode."""
    with patch('pygame.font.init'):  # Mock font initialization
        ui = GameUI(headless=True)
        assert ui.screen is None
        assert not hasattr(ui, 'score_font') or ui.score_font is None
        assert not hasattr(ui, 'winner_font') or ui.winner_font is None
        assert ui.headless


def test_headless_draw_operations(mock_pygame_setup):
    """Test that draw operations do nothing in headless mode."""
    ui = GameUI(headless=True)
    screen = mock_pygame_setup
    
    # All these operations should return immediately without error
    ui.draw_scores(5, 3)
    assert len(screen.blit_calls) == 0
    
    ui.draw_winner("Player 1")
    assert len(screen.blit_calls) == 0
    
    ball = Ball()
    paddles = [Paddle(0, 0, True), Paddle(WINDOW_WIDTH - 20, 0, False)]
    ui.draw(ball, paddles, 5, 3, True, "Player 1")
    assert len(screen.blit_calls) == 0


def test_pygame_initialization_failure(monkeypatch):
    """Test handling of pygame initialization failures."""
    def mock_init():
        raise pygame.error("Initialization failed")
    
    monkeypatch.setattr(pygame.font, "init", mock_init)
    
    with pytest.raises(pygame.error):
        GameUI(headless=False)


def test_main_draw_method(mock_pygame_setup):
    """Test the main draw method with all components."""
    ui = GameUI(headless=False)
    ui.screen = mock_pygame_setup
    
    # Create mock game objects
    ball = MagicMock()
    paddle1 = MagicMock()
    paddle2 = MagicMock()
    paddles = [paddle1, paddle2]
    
    # Draw game state
    ui.draw(ball, paddles, 5, 3, False, None)
    
    # Verify screen was cleared
    assert ui.screen.fill_color is not None
    
    # Verify separator line was drawn
    assert len(ui.screen.draw_line_calls) > 0
    line_call = ui.screen.draw_line_calls[0]
    assert line_call[0] == WHITE  # Color
    assert line_call[1][1] == GAME_AREA_TOP  # Y position
    
    # Verify game objects were drawn
    ball.draw.assert_called_once()
    paddle1.draw.assert_called_once()
    paddle2.draw.assert_called_once()


def test_draw_very_high_scores(mock_pygame_setup):
    """Test drawing very high scores doesn't break rendering."""
    ui = GameUI(headless=False)
    ui.screen = mock_pygame_setup
    
    # Test with unusually high scores
    ui.draw_scores(99999, 99999)
    
    # Verify both scores were rendered
    assert len(ui.screen.blit_calls) == 2


def test_invalid_winner_strings(mock_pygame_setup):
    """Test drawing winner with various string inputs."""
    ui = GameUI(headless=False)
    ui.screen = mock_pygame_setup
    
    # Test empty string
    ui.draw_winner("")
    assert len(ui.screen.blit_calls) == 0
    
    # Test None
    ui.draw_winner(None)
    assert len(ui.screen.blit_calls) == 0
    
    # Test very long name
    ui.draw_winner("A" * 100)  # Should still render without breaking


def test_score_positions(mock_pygame_setup):
    """Test that scores are rendered at correct positions."""
    ui = GameUI(headless=False)
    ui.screen = mock_pygame_setup
    
    ui.draw_scores(1, 2)
    
    # Verify positions of score renders
    assert len(ui.screen.blit_calls) == 2
    
    # Get positions of both scores
    _, pos1 = ui.screen.blit_calls[0]
    _, pos2 = ui.screen.blit_calls[1]
    
    # Verify x positions match constants
    assert hasattr(pos1, 'midtop')
    assert hasattr(pos2, 'midtop')
    assert pos1.midtop[0] == P1_SCORE_X
    assert pos2.midtop[0] == P2_SCORE_X
    assert pos1.midtop[1] == SCORE_MARGIN_TOP
    assert pos2.midtop[1] == SCORE_MARGIN_TOP


@patch('pygame.font.Font')
def test_font_sizes(mock_font):
    """Test that correct font sizes are used."""
    GameUI(headless=False)
    
    # Verify font sizes
    mock_font.assert_any_call(None, SCORE_FONT_SIZE)
    mock_font.assert_any_call(None, WINNER_FONT_SIZE)


def test_game_over_draw(mock_pygame_setup):
    """Test drawing the game over state."""
    ui = GameUI(headless=False)
    ui.screen = mock_pygame_setup
    
    # Create mock game objects
    ball = MagicMock()
    paddles = [MagicMock(), MagicMock()]
    
    # Draw with game over
    ui.draw(ball, paddles, 11, 5, True, "Player 1")
    
    # Verify all components were drawn
    assert ui.screen.fill_color is not None  # Screen cleared
    assert len(ui.screen.draw_line_calls) > 0  # Separator drawn
    assert len(ui.screen.blit_calls) >= 3  # Scores (2) + Winner message (1) 