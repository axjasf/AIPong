"""Records and stores gameplay data for AI learning."""

import json
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GameFrame:
    """Single frame of gameplay data."""
    state: np.ndarray  # Game state matrix
    ball_x: float
    ball_y: float
    left_paddle_y: float
    right_paddle_y: float
    left_moved_up: Optional[bool]  # None if no movement
    right_moved_up: Optional[bool]  # None if no movement
    left_hit_ball: bool
    right_hit_ball: bool

@dataclass
class GameRecord:
    """Complete record of a single point/rally."""
    frames: List[GameFrame]
    winner: Optional[str]  # "left" or "right"
    winner_hits: int  # Number of hits by the winning player
    left_hits: int  # Total ball hits by left player
    right_hits: int  # Total ball hits by right player
    timestamp: str

class GameRecorder:
    """Records and manages gameplay data."""
    
    def __init__(self):
        """Initialize the recorder."""
        self.current_game: Optional[GameRecord] = None
        self.current_frame: Optional[GameFrame] = None
        self.games_file = "human_games.json"
        
        # Load existing games if any
        try:
            with open(self.games_file, 'r') as f:
                self.recorded_games = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.recorded_games = []
    
    def start_game(self):
        """Start recording a new point/rally."""
        self.current_game = GameRecord(
            frames=[],
            winner=None,
            winner_hits=0,
            left_hits=0,
            right_hits=0,
            timestamp=datetime.now().isoformat()
        )
    
    def set_winner(self, winner: str, hits: int):
        """Set the winner of the current point/rally."""
        if self.current_game:
            self.current_game.winner = winner
            self.current_game.winner_hits = hits
    
    def update_frame(self, state: np.ndarray, ball_x: float, ball_y: float,
                    left_paddle_y: float, right_paddle_y: float,
                    left_moved_up: Optional[bool], right_moved_up: Optional[bool],
                    left_hit_ball: bool, right_hit_ball: bool):
        """Record a new frame of gameplay."""
        if self.current_game is None:
            return
            
        frame = GameFrame(
            state=state,
            ball_x=ball_x,
            ball_y=ball_y,
            left_paddle_y=left_paddle_y,
            right_paddle_y=right_paddle_y,
            left_moved_up=left_moved_up,
            right_moved_up=right_moved_up,
            left_hit_ball=left_hit_ball,
            right_hit_ball=right_hit_ball
        )
        
        self.current_game.frames.append(frame)
        
        # Track ball hits
        if left_hit_ball:
            self.current_game.left_hits += 1
        if right_hit_ball:
            self.current_game.right_hits += 1
    
    def end_game(self):
        """End the current point/rally recording and save it."""
        if self.current_game is None or len(self.current_game.frames) == 0:
            return
            
        # Only save points/rallies that had some hits
        if self.current_game.left_hits == 0 and self.current_game.right_hits == 0:
            return
            
        # Convert numpy arrays to lists for JSON serialization
        game_data = {
            'frames': [{
                'state': frame.state.tolist(),
                'ball_x': frame.ball_x,
                'ball_y': frame.ball_y,
                'left_paddle_y': frame.left_paddle_y,
                'right_paddle_y': frame.right_paddle_y,
                'left_moved_up': frame.left_moved_up,
                'right_moved_up': frame.right_moved_up,
                'left_hit_ball': frame.left_hit_ball,
                'right_hit_ball': frame.right_hit_ball
            } for frame in self.current_game.frames],
            'winner': self.current_game.winner,
            'winner_hits': self.current_game.winner_hits,
            'left_hits': self.current_game.left_hits,
            'right_hits': self.current_game.right_hits,
            'timestamp': self.current_game.timestamp
        }
        
        self.recorded_games.append(game_data)
        
        # Save to file
        with open(self.games_file, 'w') as f:
            json.dump(self.recorded_games, f)
        
        self.current_game = None 