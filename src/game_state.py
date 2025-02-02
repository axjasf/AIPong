"""Game State Matrix for AI.

This module handles the delta-matrix representation of the game state,
which shows the ball's movement and paddle positions in a discretized grid.
"""

import numpy as np
import pygame
from typing import Tuple
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    GAME_AREA_TOP, GAME_AREA_HEIGHT,
    BALL_SIZE, PADDLE_HEIGHT
)

class GameState:
    """Represents the game state as a matrix for AI input."""
    
    def __init__(self, grid_width: int = 40, grid_height: int = 30):
        """Initialize the game state matrix."""
        # Initialize basic properties
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.x_scale = grid_width / WINDOW_WIDTH
        self.y_scale = grid_height / GAME_AREA_HEIGHT
        
        # Initialize state tracking
        self.ball_x: float = 0
        self.ball_y: float = 0
        self.prev_ball_x: float = 0
        self.left_paddle_y: float = 0
        self.right_paddle_y: float = 0
        
        # Initialize collision detection
        self.ball_rect: pygame.Rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.ball_passed_paddle: bool = False
        self.ball_hit_paddle: bool = False
        
        # Initialize hit tracking
        self.left_hits: int = 0
        self.right_hits: int = 0
        
        # Initialize matrices
        self.current_matrix = np.zeros((grid_height, grid_width))
        self.previous_matrix = np.zeros((grid_height, grid_width))
        self.previous_ball_pos: Tuple[int, int] = (0, 0)
        
    def _to_grid_coords(self, x: float, y: float) -> Tuple[int, int]:
        """Convert game coordinates to grid coordinates."""
        grid_x = int(x * self.x_scale)
        grid_y = int((y - GAME_AREA_TOP) * self.y_scale)
        
        # Ensure coordinates are within grid bounds
        grid_x = max(0, min(grid_x, self.grid_width - 1))
        grid_y = max(0, min(grid_y, self.grid_height - 1))
        
        return grid_x, grid_y
    
    def update(self, ball_x: float, ball_y: float, 
               left_paddle_y: float, right_paddle_y: float) -> np.ndarray:
        """Update the state matrix with new positions.
        
        Args:
            ball_x: Ball's x position in game coordinates
            ball_y: Ball's y position in game coordinates
            left_paddle_y: Left paddle's y position in game coordinates
            right_paddle_y: Right paddle's y position in game coordinates
            
        Returns:
            The delta matrix showing ball movement (-1 for previous position,
            1 for current position) and paddle positions (2)
        """
        # Detect ball direction change (paddle hit)
        self.ball_hit_paddle = (
            (self.prev_ball_x < self.ball_x and ball_x < self.ball_x) or  # Ball changed direction from right to left
            (self.prev_ball_x > self.ball_x and ball_x > self.ball_x)     # Ball changed direction from left to right
        )
        
        # Update positions for next frame
        self.prev_ball_x = self.ball_x
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.left_paddle_y = left_paddle_y
        self.right_paddle_y = right_paddle_y
        
        # Update ball rect for collision detection
        self.ball_rect.x = int(ball_x)
        self.ball_rect.y = int(ball_y)
        
        # Track if ball passed a paddle
        prev_x = self.previous_ball_pos[0] / self.x_scale
        self.ball_passed_paddle = (
            (prev_x < WINDOW_WIDTH/4 and ball_x > WINDOW_WIDTH/4) or  # Passed left paddle
            (prev_x > 3*WINDOW_WIDTH/4 and ball_x < 3*WINDOW_WIDTH/4)  # Passed right paddle
        )
        
        # Clear the matrices
        self.previous_matrix = self.current_matrix.copy()
        self.current_matrix = np.zeros((self.grid_height, self.grid_width))
        
        # Convert coordinates to grid positions
        ball_grid_x, ball_grid_y = self._to_grid_coords(ball_x, ball_y)
        left_x, left_y = self._to_grid_coords(0, left_paddle_y)
        right_x, right_y = self._to_grid_coords(WINDOW_WIDTH - 1, right_paddle_y)
        
        # Mark paddles (use multiple cells for paddle height)
        paddle_height_cells = int(PADDLE_HEIGHT * self.y_scale)
        for i in range(paddle_height_cells):
            if 0 <= left_y + i < self.grid_height:
                self.current_matrix[left_y + i, left_x] = 2
            if 0 <= right_y + i < self.grid_height:
                self.current_matrix[right_y + i, right_x] = 2
        
        # Mark current ball position
        self.current_matrix[ball_grid_y, ball_grid_x] = 1
        
        # Create delta matrix
        delta_matrix = self.current_matrix.copy()
        prev_x, prev_y = self.previous_ball_pos
        if 0 <= prev_y < self.grid_height and 0 <= prev_x < self.grid_width:
            delta_matrix[prev_y, prev_x] = -1
        
        # Update previous ball position
        self.previous_ball_pos = (ball_grid_y, ball_grid_x)
        
        return delta_matrix 