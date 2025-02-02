"""Game state handling.

This module contains the GameState class that handles:
- Game state matrix representation
- State updates based on game objects
- State normalization for AI input
"""

import numpy as np
from typing import List, Tuple

from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    BALL_SIZE,
)


class GameState:
    """Handles the game state matrix and updates."""

    def __init__(self) -> None:
        """Initialize the game state system."""
        self.state_size = 6  # [ball_x, ball_y, ball_dx, ball_dy, left_paddle_y, right_paddle_y]
        self.state = np.zeros(self.state_size)
        self.prev_ball_pos = (0, 0)

    def normalize_coordinates(
        self, x: float, y: float, width: float = 0, height: float = 0
    ) -> Tuple[float, float]:
        """Normalize coordinates to [-1, 1] range."""
        # Normalize x position to [-1, 1]
        norm_x = (x + width / 2) / (WINDOW_WIDTH / 2) - 1

        # Normalize y position to [-1, 1], accounting for game area
        playable_height = GAME_AREA_HEIGHT - height
        norm_y = (
            2
            * (y - GAME_AREA_TOP - height / 2)
            / playable_height
            - 1
        )

        return norm_x, norm_y

    def update(
        self, ball_x: float, ball_y: float, left_paddle_y: float, right_paddle_y: float
    ) -> np.ndarray:
        """Update the game state matrix."""
        # Calculate ball velocity
        ball_dx = ball_x - self.prev_ball_pos[0]
        ball_dy = ball_y - self.prev_ball_pos[1]
        self.prev_ball_pos = (ball_x, ball_y)

        # Normalize positions
        norm_ball_x, norm_ball_y = self.normalize_coordinates(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
        _, norm_left_y = self.normalize_coordinates(
            PADDLE_WIDTH, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT
        )
        _, norm_right_y = self.normalize_coordinates(
            WINDOW_WIDTH - PADDLE_WIDTH,
            right_paddle_y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
        )

        # Normalize velocities
        norm_ball_dx = ball_dx / WINDOW_WIDTH
        norm_ball_dy = ball_dy / GAME_AREA_HEIGHT

        # Update state
        self.state = np.array(
            [
                norm_ball_x,
                norm_ball_y,
                norm_ball_dx,
                norm_ball_dy,
                norm_left_y,
                norm_right_y,
            ]
        )

        return self.state

    def get_state(self) -> np.ndarray:
        """Get the current game state."""
        return self.state.copy()

    def get_state_size(self) -> int:
        """Get the size of the state vector."""
        return self.state_size
