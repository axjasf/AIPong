"""Paddle handling system.

This module contains the Paddle class that handles:
- Paddle movement
- Position constraints
- Collision detection
"""

from typing import Optional, Tuple

import pygame

from .constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_COLOR,
)


class Paddle:
    """Handles paddle movement and collision detection."""

    def __init__(self, x: float, y: float, is_left: bool = True) -> None:
        """Initialize the paddle.

        Args:
            x: Initial x position
            y: Initial y position
            is_left: Whether this is the left paddle (default: True)
        """
        self.x = float(x)
        self.y = float(y)
        self.is_left = is_left
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = float(PADDLE_SPEED)
        self.color = PADDLE_COLOR

        # Create pygame rect for collision detection
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)

    def move_up(self) -> None:
        """Move the paddle up."""
        new_y = self.y - self.speed
        self.set_y(new_y)

    def move_down(self) -> None:
        """Move the paddle down."""
        new_y = self.y + self.speed
        self.set_y(new_y)

    def update_ai(self, ball_y: float) -> None:
        """Update AI paddle position based on ball position.

        Args:
            ball_y: The y position of the ball
        """
        paddle_center = self.y + (self.height / 2)
        if ball_y < paddle_center - 10:  # Add small deadzone
            self.move_up()
        elif ball_y > paddle_center + 10:
            self.move_down()

    def get_y(self) -> float:
        """Get the paddle's y position.

        Returns:
            Current y position as float
        """
        return self.y

    def set_y(self, y: float) -> None:
        """Set the paddle's y position within game area bounds.

        Args:
            y: New y position
        """
        # Ensure paddle stays within game area
        self.y = max(
            float(GAME_AREA_TOP),
            min(float(y), float(GAME_AREA_TOP + GAME_AREA_HEIGHT - self.height)),
        )
        # Update collision rect
        self.rect.y = int(self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the paddle on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def get_collision_point(self, ball_rect: pygame.Rect) -> Optional[Tuple[float, float]]:
        """Get the point of collision with a ball.

        Args:
            ball_rect: The ball's collision rectangle

        Returns:
            Tuple of (x, y) collision point if collision occurred, None otherwise
        """
        if not self.rect.colliderect(ball_rect):
            return None

        # Calculate collision point
        if self.is_left:
            x = float(self.rect.right)
        else:
            x = float(self.rect.left)

        # Calculate y position at point of collision
        y = float(ball_rect.centery)

        return x, y

    def get_relative_hit_position(self, ball_rect: pygame.Rect) -> Optional[float]:
        """Get the relative position where the ball hit the paddle.

        Args:
            ball_rect: The ball's collision rectangle

        Returns:
            Float between -1 and 1 indicating where the ball hit (-1 = top, 1 = bottom),
            or None if no collision
        """
        collision = self.get_collision_point(ball_rect)
        if not collision:
            return None

        # Calculate relative position (-1 to 1)
        _, y = collision
        relative_pos = (y - float(self.rect.top)) / float(self.height)
        return 2 * relative_pos - 1  # Convert from [0,1] to [-1,1]
