"""Game state handling.

This module contains the GameState class that handles:
- Game state matrix representation
- State updates based on game objects
- State normalization for AI input
"""

from typing import Tuple

import numpy as np
import pygame

from .constants import (
    WINDOW_WIDTH,
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
        self.state: np.ndarray = np.zeros(self.state_size, dtype=np.float32)
        self.prev_ball_pos = (0.0, 0.0)

        # Ball properties
        self.ball_x = 0.0
        self.ball_y = 0.0
        self.ball_dx = 0.0
        self.ball_dy = 0.0
        self.ball_rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)

        # Paddle positions
        self.left_paddle_y = 0.0
        self.right_paddle_y = 0.0

        # Hit counters
        self.left_hits = 0
        self.right_hits = 0

    def normalize_coordinates(
        self, x: float, y: float, width: float = 0, height: float = 0
    ) -> Tuple[float, float]:
        """Normalize coordinates to [-1, 1] range.

        Args:
            x: X coordinate to normalize
            y: Y coordinate to normalize
            width: Width of the object
            height: Height of the object

        Returns:
            Tuple of normalized (x, y) coordinates
        """
        # Normalize x position to [-1, 1]
        norm_x = (x + width / 2) / (WINDOW_WIDTH / 2) - 1

        # Normalize y position to [-1, 1], accounting for game area
        playable_height = float(GAME_AREA_HEIGHT - height)
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
        """Update the game state matrix.

        Args:
            ball_x: Ball's x position
            ball_y: Ball's y position
            left_paddle_y: Left paddle's y position
            right_paddle_y: Right paddle's y position

        Returns:
            Updated state matrix
        """
        # Update stored positions
        self.ball_x = float(ball_x)
        self.ball_y = float(ball_y)
        self.left_paddle_y = float(left_paddle_y)
        self.right_paddle_y = float(right_paddle_y)

        # Update ball rect
        self.ball_rect.x = int(ball_x)
        self.ball_rect.y = int(ball_y)

        # Calculate ball velocity
        self.ball_dx = self.ball_x - self.prev_ball_pos[0]
        self.ball_dy = self.ball_y - self.prev_ball_pos[1]
        self.prev_ball_pos = (self.ball_x, self.ball_y)

        # Normalize positions
        norm_ball_x, norm_ball_y = self.normalize_coordinates(
            self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE
        )
        _, norm_left_y = self.normalize_coordinates(
            PADDLE_WIDTH,
            self.left_paddle_y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
        )
        _, norm_right_y = self.normalize_coordinates(
            WINDOW_WIDTH - PADDLE_WIDTH,
            self.right_paddle_y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
        )

        # Normalize velocities
        norm_ball_dx = self.ball_dx / WINDOW_WIDTH
        norm_ball_dy = self.ball_dy / GAME_AREA_HEIGHT

        # Update state
        self.state = np.array(
            [
                norm_ball_x,
                norm_ball_y,
                norm_ball_dx,
                norm_ball_dy,
                norm_left_y,
                norm_right_y,
            ],
            dtype=np.float32,
        )

        return self.state

    def get_state(self) -> np.ndarray:
        """Get the current game state.

        Returns:
            Copy of the current state matrix
        """
        return self.state.copy()

    def get_state_size(self) -> int:
        """Get the size of the state vector.

        Returns:
            Size of the state vector
        """
        return self.state_size

    def increment_hits(self, is_left_paddle: bool) -> None:
        """Increment the hit counter for the specified paddle.

        Args:
            is_left_paddle: Whether the left paddle hit the ball
        """
        if is_left_paddle:
            self.left_hits += 1
        else:
            self.right_hits += 1

    def reset_hits(self) -> None:
        """Reset hit counters for both paddles."""
        self.left_hits = 0
        self.right_hits = 0
