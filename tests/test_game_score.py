"""Test suite for game score."""

import pytest
from src.game_score import GameScore


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