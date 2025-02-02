"""Paddle class for Pong game."""

import pygame
from .constants import PADDLE_WIDTH, PADDLE_HEIGHT, WHITE, PADDLE_SPEED


class Paddle:
    """Represents a paddle in the game."""

    def __init__(self, x: int, y: int, min_y: int, max_y: int) -> None:
        """Initialize the paddle.

        Args:
            x: X position of paddle
            y: Y position of paddle
            min_y: Minimum Y position (top boundary)
            max_y: Maximum Y position (bottom boundary)
        """
        self.x: int = x
        self.y: float = float(y)  # Store as float for smooth movement
        self.min_y: int = min_y
        self.max_y: int = max_y - PADDLE_HEIGHT
        self.rect: pygame.Rect = pygame.Rect(x, int(self.y), PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up: bool) -> None:
        """Move the paddle up or down.

        Args:
            up: True to move up, False to move down
        """
        if up and self.y > self.min_y:
            self.y -= PADDLE_SPEED
        elif not up and self.y < self.max_y:
            self.y += PADDLE_SPEED

        self.rect.y = int(self.y)

    def get_y(self) -> float:
        """Get the current Y position."""
        return self.y

    def set_y(self, y: float) -> None:
        """Set the Y position.

        Args:
            y: New Y position
        """
        self.y = max(float(self.min_y), min(y, float(self.max_y)))
        self.rect.y = int(self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the paddle on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, WHITE, self.rect)
