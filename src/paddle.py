"""Pong Game Paddle Class.

This module contains the Paddle class that handles:
- Paddle movement within game boundaries
- Paddle rendering
- Movement speed and constraints
"""

import pygame
from typing import Optional
from .constants import (
    # Game Objects
    PADDLE_WIDTH, PADDLE_HEIGHT,
    PADDLE_SPEED, PADDLE_COLOR
)

class Paddle:
    """Represents a paddle with position and movement controls."""
    
    def __init__(self, x: int, y: int, min_y: int, max_y: int) -> None:
        """Initialize the paddle with starting position and movement bounds."""
        self.x: int = x
        self.y: int = y
        self.min_y: int = min_y
        self.max_y: int = max_y - PADDLE_HEIGHT
        self.speed: int = PADDLE_SPEED
        self.rect: pygame.Rect = pygame.Rect(x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    def move(self, up: bool = False) -> None:
        """Move the paddle up or down within screen bounds."""
        if up and self.y > self.min_y:
            self.y = max(self.min_y, self.y - self.speed)
        elif not up and self.y < self.max_y:
            self.y = min(self.max_y, self.y + self.speed)
        self.rect.y = self.y
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the paddle on the screen."""
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect) 