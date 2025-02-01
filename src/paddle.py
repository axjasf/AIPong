"""Paddle class for the Pong game."""

import pygame
from typing import Optional
from .constants import (
    PADDLE_WIDTH, PADDLE_HEIGHT, WINDOW_HEIGHT,
    PADDLE_SPEED, PADDLE_COLOR
)

class Paddle:
    """Represents a paddle with position and movement controls."""
    
    def __init__(self, x: int) -> None:
        """Initialize the paddle with starting x position."""
        self.x: int = x
        self.y: int = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.speed: int = PADDLE_SPEED
        self.rect: pygame.Rect = pygame.Rect(x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    def move(self, up: bool = False) -> None:
        """Move the paddle up or down within screen bounds."""
        if up and self.y > 0:
            self.y -= self.speed
        elif not up and self.y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            self.y += self.speed
        self.rect.y = self.y
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the paddle on the screen."""
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect) 