"""Game state recording system.

This module contains the GameRecorder class that handles:
- Recording game states
- Recording paddle actions
- Recording game outcomes
- Saving training data
"""

import json
import logging
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


class GameRecorder:
    """Records game states and actions for training data collection."""

    def __init__(self, output_dir: str = "training_data") -> None:
        """Initialize the game recorder.

        Args:
            output_dir: Directory to save training data (default: "training_data")
        """
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize game recording
        self.current_game: List[Dict[str, Union[np.ndarray, Optional[bool], int, float]]] = []
        self.games: List[List[Dict[str, Union[np.ndarray, Optional[bool], int, float]]]] = []
        self.game_count = 0
        self.current_winner: Optional[str] = None
        self.current_hits = 0

    def start_game(self) -> None:
        """Start recording a new game/point."""
        self.current_game = []
        self.current_winner = None
        self.current_hits = 0

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
        """Record a single frame of game state and actions.

        Args:
            state: Game state matrix
            ball_x: Ball x position
            ball_y: Ball y position
            left_paddle_y: Left paddle y position
            right_paddle_y: Right paddle y position
            left_moved_up: Whether left paddle moved up (None if no movement)
            right_moved_up: Whether right paddle moved up (None if no movement)
            left_hit_ball: Whether left paddle hit the ball
            right_hit_ball: Whether right paddle hit the ball
        """
        frame_data = {
            "state": state,
            "ball_pos": (ball_x, ball_y),
            "paddle_pos": (left_paddle_y, right_paddle_y),
            "left_action": left_moved_up,
            "right_action": right_moved_up,
            "left_hit": int(left_hit_ball),
            "right_hit": int(right_hit_ball),
        }
        self.current_game.append(frame_data)

    def set_winner(self, side: str, hits: int) -> None:
        """Set the winner of the current game/point.

        Args:
            side: Which side won ("left" or "right")
            hits: Number of hits in the rally
        """
        self.current_winner = side
        self.current_hits = hits

    def end_game(self) -> None:
        """End the current game/point and save it if valid."""
        if not self.current_game:
            return

        # Only save games with a winner and at least one frame
        if self.current_winner and len(self.current_game) > 0:
            self.games.append(self.current_game)
            self.game_count += 1

            # Save every 100 games
            if self.game_count % 100 == 0:
                self.save_games()

    def save_games(self) -> None:
        """Save recorded games to disk."""
        if not self.games:
            return

        # Create a unique filename
        filename = self.output_dir / f"pong_games_{self.game_count}.npz"

        try:
            # Convert game data to numpy arrays
            states = []
            actions = []
            outcomes = []
            metadata = []

            for game in self.games:
                game_states = []
                game_actions = []
                game_outcomes = []
                game_metadata = []

                for frame in game:
                    # State is already numpy array
                    game_states.append(frame["state"])

                    # Convert actions to one-hot
                    left_action = frame["left_action"]
                    right_action = frame["right_action"]
                    left_one_hot = [1, 0, 0] if left_action is None else [0, 1, 0] if left_action else [0, 0, 1]
                    right_one_hot = [1, 0, 0] if right_action is None else [0, 1, 0] if right_action else [0, 0, 1]
                    game_actions.append(left_one_hot + right_one_hot)

                    # Outcome is winner side
                    game_outcomes.append(1 if self.current_winner == "left" else -1)

                    # Metadata includes positions and hits
                    game_metadata.append(
                        [
                            *frame["ball_pos"],
                            *frame["paddle_pos"],
                            frame["left_hit"],
                            frame["right_hit"],
                        ]
                    )

                states.append(np.array(game_states))
                actions.append(np.array(game_actions))
                outcomes.append(np.array(game_outcomes))
                metadata.append(np.array(game_metadata))

            # Save arrays
            np.savez_compressed(
                filename,
                states=np.array(states),
                actions=np.array(actions),
                outcomes=np.array(outcomes),
                metadata=np.array(metadata),
            )

            self.logger.info("Saved %d games to %s", len(self.games), filename)

            # Clear saved games
            self.games = []

        except Exception as e:
            self.logger.error("Failed to save games: %s", e)

    def __del__(self) -> None:
        """Save any remaining games on deletion."""
        self.save_games()
