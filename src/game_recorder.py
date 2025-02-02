"""Game recorder for saving and loading gameplay data."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import json

import numpy as np


@dataclass
class GameFrame:
    """A single frame of gameplay data."""

    state: np.ndarray
    ball_x: float
    ball_y: float
    left_paddle_y: float
    right_paddle_y: float
    left_moved_up: Optional[bool]
    right_moved_up: Optional[bool]
    left_hit_ball: bool
    right_hit_ball: bool


class GameRecorder:
    """Records gameplay data for AI training."""

    def __init__(self) -> None:
        """Initialize the game recorder."""
        self.current_game_frames: List[GameFrame] = []
        self.games: List[dict] = []
        self.recording = False
        self.left_hits = 0
        self.right_hits = 0
        self.winner: Optional[str] = None

    def start_game(self) -> None:
        """Start recording a new game/point."""
        self.current_game_frames = []
        self.recording = True
        self.left_hits = 0
        self.right_hits = 0
        self.winner = None

    def end_game(self) -> None:
        """End recording the current game/point."""
        if not self.recording:
            return

        # Save the current game data
        game_data = {
            "timestamp": datetime.now().isoformat(),
            "frames": [
                {
                    "state": frame.state.tolist(),
                    "ball_x": frame.ball_x,
                    "ball_y": frame.ball_y,
                    "left_paddle_y": frame.left_paddle_y,
                    "right_paddle_y": frame.right_paddle_y,
                    "left_moved_up": frame.left_moved_up,
                    "right_moved_up": frame.right_moved_up,
                    "left_hit_ball": frame.left_hit_ball,
                    "right_hit_ball": frame.right_hit_ball,
                }
                for frame in self.current_game_frames
            ],
            "winner": self.winner,
            "left_hits": self.left_hits,
            "right_hits": self.right_hits,
        }

        self.games.append(game_data)
        self.recording = False

        # Save to file after each game/point
        self._save_to_file()

    def update_frame(
        self,
        state: np.ndarray,
        ball_x: float,
        ball_y: float,
        left_paddle_y: float,
        right_paddle_y: float,
        left_moved_up: Optional[bool],
        right_moved_up: Optional[bool],
        left_hit_ball: bool,
        right_hit_ball: bool,
    ) -> None:
        """Record a single frame of gameplay."""
        if not self.recording:
            return

        frame = GameFrame(
            state=state.copy(),
            ball_x=ball_x,
            ball_y=ball_y,
            left_paddle_y=left_paddle_y,
            right_paddle_y=right_paddle_y,
            left_moved_up=left_moved_up,
            right_moved_up=right_moved_up,
            left_hit_ball=left_hit_ball,
            right_hit_ball=right_hit_ball,
        )

        self.current_game_frames.append(frame)

        if left_hit_ball:
            self.left_hits += 1
        if right_hit_ball:
            self.right_hits += 1

    def set_winner(self, side: str, hits: int) -> None:
        """Set the winner of the current game/point."""
        self.winner = side
        if side == "left":
            self.left_hits = hits
        else:
            self.right_hits = hits

    def _save_to_file(self, filename: str = "human_games.json") -> None:
        """Save recorded games to a file."""
        try:
            # Load existing games if file exists
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    existing_games = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_games = []

            # Add new games
            existing_games.extend(self.games)

            # Save all games
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(existing_games, f, indent=2)

            # Clear saved games
            self.games = []

        except Exception as e:
            print(f"Error saving gameplay data: {e}")
