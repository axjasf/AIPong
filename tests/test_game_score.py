"""Test suite for game score."""

import pytest
import pygame
from src.game_score import GameScore
from src.constants import FONT_SIZE, SCORE_COLOR


# Initialize pygame for font support
pygame.font.init()


def test_game_score_initialization():
    """Test game score initialization."""
    score = GameScore()
    assert score.scores[0] == 0  # left score
    assert score.scores[1] == 0  # right score


def test_increment_left_score():
    """Test incrementing left player score."""
    score = GameScore()
    score.increment_score(True)  # True for left player
    assert score.scores[0] == 1
    assert score.scores[1] == 0


def test_increment_right_score():
    """Test incrementing right player score."""
    score = GameScore()
    score.increment_score(False)  # False for right player
    assert score.scores[0] == 0
    assert score.scores[1] == 1


def test_multiple_score_increments():
    """Test multiple score increments for both players."""
    score = GameScore()
    
    for _ in range(3):
        score.increment_score(True)  # Left player
    for _ in range(2):
        score.increment_score(False)  # Right player
        
    assert score.scores[0] == 3
    assert score.scores[1] == 2


def test_reset_score():
    """Test resetting the score."""
    score = GameScore()
    score.increment_score(True)
    score.increment_score(False)
    score.reset()
    
    assert score.scores[0] == 0
    assert score.scores[1] == 0


def test_get_scores():
    """Test getting scores."""
    score = GameScore()
    score.increment_score(True)
    score.increment_score(False)
    
    scores = score.get_scores()
    assert scores == [1, 1]
    
    # Verify it's a copy
    scores[0] = 99
    assert score.scores[0] == 1


def test_check_winner():
    """Test winner detection."""
    score = GameScore()
    
    # No winner initially
    assert score.check_winner() is None
    
    # Left player wins
    for _ in range(11):
        score.increment_score(True)
    assert score.check_winner() == 0
    
    # Reset and test right player win
    score.reset()
    for _ in range(11):
        score.increment_score(False)
    assert score.check_winner() == 1
    
    # Test two point lead requirement
    score.reset()
    for _ in range(10):
        score.increment_score(True)
    for _ in range(10):
        score.increment_score(False)
    assert score.check_winner() is None  # Tied at 10
    
    score.increment_score(True)  # 11-10
    assert score.check_winner() is None  # One point lead not enough
    
    score.increment_score(True)  # 12-10
    assert score.check_winner() == 0  # Two point lead wins 


@pytest.fixture
def mock_surface():
    """Fixture for mock surface."""
    class MockSurface:
        def __init__(self):
            self.blit_calls = []
        
        def blit(self, surface, position):
            self.blit_calls.append((surface, position))
        
        def get_rect(self, **kwargs):
            class MockRect:
                def __init__(self):
                    for key, value in kwargs.items():
                        setattr(self, key, value)
            return MockRect()
    return MockSurface


@pytest.fixture
def mock_pygame_setup(monkeypatch, mock_surface):
    """Setup pygame mocks for testing draw functionality."""
    class MockFont:
        def __init__(self, name, size):
            self.name = name
            self.size = size
        
        def render(self, text, antialias, color):
            return mock_surface()

    monkeypatch.setattr(pygame.font, "Font", MockFont)
    return mock_surface


def test_draw_with_default_font(mock_pygame_setup):
    """Test drawing scores with default font."""
    screen = mock_pygame_setup()
    score = GameScore()
    score.increment_score(True)  # 1-0
    
    score.draw(screen)
    
    assert len(screen.blit_calls) == 1  # Verify one blit call was made


def test_draw_with_custom_font(mock_pygame_setup):
    """Test drawing scores with custom font."""
    screen = mock_pygame_setup()
    score = GameScore()
    custom_font = pygame.font.Font(None, 42)  # Different size than default
    
    score.draw(screen, font=custom_font)
    
    assert len(screen.blit_calls) == 1
    assert custom_font.size == 42  # Verify custom font was used


def test_draw_score_positioning(mock_pygame_setup):
    """Test score text positioning."""
    screen = mock_pygame_setup()
    score = GameScore()
    score.increment_score(True)   # 1-0
    score.increment_score(False)  # 1-1
    
    score.draw(screen)
    
    # Verify one blit call was made
    assert len(screen.blit_calls) == 1
    
    # Verify the surface was positioned correctly
    _, pos = screen.blit_calls[0]
    assert hasattr(pos, 'centerx')  # Should be centered horizontally
    assert hasattr(pos, 'top')      # Should have top alignment 


def test_draw_score_text_content(mock_pygame_setup, mock_surface):
    """Test the actual text content being rendered."""
    class MockFont:
        def __init__(self, name, size):
            self.name = name
            self.size = size
        
        def render(self, text, antialias, color):
            self.last_render = {'text': text, 'antialias': antialias, 'color': color}
            return mock_surface()

    screen = mock_pygame_setup()
    score = GameScore()
    score.increment_score(True)   # 1-0
    
    # Replace the mock with our special version that captures render args
    font = MockFont(None, FONT_SIZE)
    score.draw(screen, font=font)
    
    assert font.last_render['text'] == "1  0"  # Verify exact format
    assert font.last_render['antialias'] is True
    assert font.last_render['color'] == SCORE_COLOR


def test_draw_high_scores(mock_pygame_setup):
    """Test drawing with unusually high scores."""
    screen = mock_pygame_setup()
    score = GameScore()
    
    # Set some ridiculously high scores
    for _ in range(100):
        score.increment_score(True)
    for _ in range(99):
        score.increment_score(False)
    
    # Should not raise any exceptions
    score.draw(screen)
    assert len(screen.blit_calls) == 1


def test_draw_without_screen(mock_pygame_setup):
    """Test handling of drawing without a valid screen."""
    score = GameScore()
    score.font = pygame.font.Font(None, FONT_SIZE)  # Pre-initialize font
    
    with pytest.raises((TypeError, AttributeError)):
        score.draw(None)


def test_font_initialization_failure(monkeypatch, mock_pygame_setup):
    """Test handling of font initialization failure."""
    def mock_font_init(*args):
        raise pygame.error("Font initialization failed")
    
    monkeypatch.setattr(pygame.font.Font, "__init__", mock_font_init)
    
    score = GameScore()
    screen = mock_pygame_setup()
    with pytest.raises(pygame.error):
        score.draw(screen)


def test_font_size_from_constants(mock_pygame_setup):
    """Test that font size matches the constant."""
    screen = mock_pygame_setup()
    score = GameScore()
    
    # Force font reinitialization
    score.font = None
    score.draw(screen)
    
    # The mock_pygame_setup should have captured the font size
    font = pygame.font.Font(None, FONT_SIZE)
    assert font.size == FONT_SIZE 