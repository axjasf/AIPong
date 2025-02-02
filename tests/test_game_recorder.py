"""Test suite for game recorder."""

import pytest
import os
import json
from src.game_recorder import GameRecorder
from src.game_types import BallState, PaddleState


@pytest.fixture
def game_recorder():
    """Fixture for game recorder."""
    recorder = GameRecorder()
    yield recorder
    # Cleanup any test files
    if os.path.exists(recorder.filename):
        os.remove(recorder.filename)


@pytest.fixture
def sample_states():
    """Fixture for sample game states."""
    ball_states = [
        BallState(x=400, y=300),
        BallState(x=410, y=305),
        BallState(x=420, y=310)
    ]
    paddle_states = [
        PaddleState(left_y=250, right_y=250),
        PaddleState(left_y=255, right_y=245),
        PaddleState(left_y=260, right_y=240)
    ]
    return ball_states, paddle_states


def test_game_recorder_initialization(game_recorder):
    """Test game recorder initialization."""
    assert game_recorder.states == []
    assert game_recorder.filename.endswith(".json")


def test_record_state(game_recorder, sample_states):
    """Test recording game states."""
    ball_states, paddle_states = sample_states
    
    for ball_state, paddle_state in zip(ball_states, paddle_states):
        game_recorder.record_state(ball_state, paddle_state)
    
    assert len(game_recorder.states) == 3
    
    # Verify first recorded state
    first_state = game_recorder.states[0]
    assert first_state["ball"]["x"] == 400
    assert first_state["ball"]["y"] == 300
    assert first_state["paddle"]["left_y"] == 250
    assert first_state["paddle"]["right_y"] == 250


def test_save_and_load_recording(game_recorder, sample_states):
    """Test saving and loading game recording."""
    ball_states, paddle_states = sample_states
    
    # Record some states
    for ball_state, paddle_state in zip(ball_states, paddle_states):
        game_recorder.record_state(ball_state, paddle_state)
    
    # Save recording
    game_recorder.save_recording()
    assert os.path.exists(game_recorder.filename)
    
    # Verify file contents
    with open(game_recorder.filename, 'r') as f:
        saved_data = json.load(f)
        assert len(saved_data) == 3
        assert saved_data[0]["ball"]["x"] == 400
        assert saved_data[1]["ball"]["x"] == 410
        assert saved_data[2]["ball"]["x"] == 420


def test_reset_recording(game_recorder, sample_states):
    """Test resetting game recording."""
    ball_states, paddle_states = sample_states
    
    # Record some states
    for ball_state, paddle_state in zip(ball_states, paddle_states):
        game_recorder.record_state(ball_state, paddle_state)
    
    # Reset recording
    game_recorder.reset_recording()
    assert len(game_recorder.states) == 0


def test_record_state_format(game_recorder):
    """Test the format of recorded states."""
    ball_state = BallState(x=100, y=200, prev_x=90)
    paddle_state = PaddleState(left_y=300, right_y=400, left_hits=1, right_hits=2)
    
    game_recorder.record_state(ball_state, paddle_state)
    recorded_state = game_recorder.states[0]
    
    assert recorded_state["ball"]["x"] == 100
    assert recorded_state["ball"]["y"] == 200
    assert recorded_state["ball"]["prev_x"] == 90
    assert recorded_state["paddle"]["left_y"] == 300
    assert recorded_state["paddle"]["right_y"] == 400
    assert recorded_state["paddle"]["left_hits"] == 1
    assert recorded_state["paddle"]["right_hits"] == 2 