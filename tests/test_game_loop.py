"""Test suite for game loop."""

import pytest
import pygame
from unittest.mock import MagicMock, patch
from src.game_loop import GameLoop
from src.game import Game
from src.constants import FPS


@pytest.fixture
def game_loop():
    """Fixture for game loop instance."""
    pygame.init()
    loop = GameLoop()
    yield loop
    pygame.quit()


def test_game_loop_initialization(game_loop):
    """Test game loop initialization."""
    assert game_loop.clock is not None
    assert game_loop.fps == FPS


@patch('pygame.event.get')
def test_handle_events_quit(mock_event_get, game_loop):
    """Test handling quit event."""
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT
    mock_event_get.return_value = [mock_event]
    
    # Handle events should return False for quit
    assert not game_loop.handle_events()


@patch('pygame.event.get')
def test_handle_events_keydown(mock_event_get, game_loop):
    """Test handling keydown events."""
    # Test pause key
    mock_pause_event = MagicMock()
    mock_pause_event.type = pygame.KEYDOWN
    mock_pause_event.key = pygame.K_SPACE
    mock_event_get.return_value = [mock_pause_event]
    
    assert game_loop.handle_events()  # Should return True and toggle pause
    assert game_loop.game.paused
    
    # Test reset key
    mock_reset_event = MagicMock()
    mock_reset_event.type = pygame.KEYDOWN
    mock_reset_event.key = pygame.K_r
    mock_event_get.return_value = [mock_reset_event]
    
    game_loop.game.game_over = True
    assert game_loop.handle_events()  # Should return True and reset game
    assert not game_loop.game.game_over


@patch('pygame.event.get')
def test_handle_events_multiple(mock_event_get, game_loop):
    """Test handling multiple events."""
    mock_events = [
        MagicMock(type=pygame.KEYDOWN, key=pygame.K_SPACE),
        MagicMock(type=pygame.KEYDOWN, key=pygame.K_r)
    ]
    mock_event_get.return_value = mock_events
    
    assert game_loop.handle_events()  # Should handle both events
    assert game_loop.game.paused  # Space key should have toggled pause


def test_update(game_loop):
    """Test game loop update."""
    # Test update when not paused
    assert not game_loop.game.paused
    initial_ball_x = game_loop.game.ball.x
    game_loop.update()
    assert game_loop.game.ball.x != initial_ball_x  # Ball should move
    
    # Test update when paused
    game_loop.game.paused = True
    ball_x_before_pause = game_loop.game.ball.x
    game_loop.update()
    assert game_loop.game.ball.x == ball_x_before_pause  # Ball should not move


@patch('pygame.display.flip')
@patch('pygame.Surface.fill')
@patch('pygame.draw.rect')
@patch('pygame.draw.circle')
def test_render(mock_circle, mock_rect, mock_fill, mock_flip, game_loop):
    """Test game loop render."""
    game_loop.render()
    
    # Verify that all drawing functions were called
    assert mock_fill.called
    assert mock_rect.called
    assert mock_circle.called
    assert mock_flip.called


def test_maintain_framerate(game_loop):
    """Test frame rate maintenance."""
    initial_time = pygame.time.get_ticks()
    game_loop.maintain_framerate()
    final_time = pygame.time.get_ticks()
    
    # Time difference should be less than or equal to the frame time
    max_frame_time = 1000 / game_loop.fps  # milliseconds per frame
    assert final_time - initial_time <= max_frame_time


@patch('pygame.event.get')
def test_game_loop_integration(mock_event_get, game_loop):
    """Test game loop integration."""
    # Mock events to run for a few frames then quit
    mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_w)]  # Some gameplay event
    mock_quit_event = MagicMock(type=pygame.QUIT)
    
    def event_sequence():
        """Return gameplay events for 3 frames, then quit."""
        nonlocal mock_events
        if hasattr(event_sequence, 'count'):
            event_sequence.count += 1
        else:
            event_sequence.count = 0
        
        if event_sequence.count < 3:
            return mock_events
        return [mock_quit_event]
    
    mock_event_get.side_effect = event_sequence
    
    # Run game loop
    frames = 0
    while game_loop.handle_events():
        game_loop.update()
        game_loop.render()
        game_loop.maintain_framerate()
        frames += 1
    
    assert frames == 3  # Should run for 3 frames before quit 