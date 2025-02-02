"""Pong Game Paddle Class.

This module contains the Paddle class that handles:
- Paddle movement within game boundaries
- Paddle rendering
- Movement speed and constraints
"""

import pygame
from typing import Optional
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    GAME_AREA_TOP, GAME_AREA_HEIGHT,
    PADDLE_WIDTH, PADDLE_HEIGHT,
    PADDLE_SPEED, PADDLE_COLOR
)

class Paddle:
    """Represents a paddle with position and movement controls."""
    
    def __init__(self, x: int, y: int, min_y: int, max_y: int, grid_height: int = 30) -> None:
        """Initialize the paddle with starting position and movement bounds."""
        # Store grid coordinates
        self.grid_height = grid_height
        self.y_scale = grid_height / GAME_AREA_HEIGHT
        
        # Convert screen coordinates to grid coordinates
        self.grid_y = int((y - GAME_AREA_TOP) * self.y_scale)
        self.min_grid_y = int((min_y - GAME_AREA_TOP) * self.y_scale)
        self.max_grid_y = int((max_y - GAME_AREA_TOP - PADDLE_HEIGHT) * self.y_scale)
        
        # Keep screen x for rendering
        self.x = x
        
        # Create rect for rendering and collision
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self._update_rect()
    
    def _update_rect(self) -> None:
        """Update the pygame rect based on grid position."""
        # Convert grid coordinates back to screen coordinates for rendering
        screen_y = (self.grid_y / self.y_scale) + GAME_AREA_TOP
        self.rect.y = int(screen_y)
    
    def move(self, up: bool = False) -> None:
        """Move the paddle up or down within grid bounds."""
        if up and self.grid_y > self.min_grid_y:
            self.grid_y = max(self.min_grid_y, self.grid_y - 1)
        elif not up and self.grid_y < self.max_grid_y:
            self.grid_y = min(self.max_grid_y, self.grid_y + 1)
        self._update_rect()
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the paddle on the screen."""
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)
    
    def get_y(self) -> int:
        """Get screen y coordinate."""
        return self.rect.y
    
    def set_y(self, screen_y: int) -> None:
        """Set screen y coordinate and update grid position."""
        self.grid_y = int((screen_y - GAME_AREA_TOP) * self.y_scale)
        self._update_rect() 