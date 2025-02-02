"""Ball handling system.

This module contains the Ball class that handles:
- Ball movement
- Collision physics
- Speed and angle calculations
"""

import logging
import math
import random
from typing import List, Optional

import pygame

from .constants import (
    WINDOW_WIDTH,
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    BALL_SIZE,
    BALL_SPEED,
    BALL_MAX_SPEED,
    BALL_SPEED_INCREASE,
    BALL_COLOR,
)
from .paddle import Paddle


class Ball:
    """Handles ball movement and collision physics."""

    def __init__(self) -> None:
        """Initialize the ball."""
        self.logger = logging.getLogger(__name__)
        self.size = BALL_SIZE
        self.speed = float(BALL_SPEED)
        self.max_speed = float(BALL_MAX_SPEED)
        self.speed_increase = float(BALL_SPEED_INCREASE)
        self.color = BALL_COLOR

        # Create pygame rect for collision detection
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        
        # Initialize position and velocity
        self.x = 0.0
        self.y = 0.0
        self.dx = 0.0
        self.dy = 0.0
        
        # Reset to starting position
        self.reset()

    def _normalize_velocity(self) -> None:
        """Normalize velocity components to match exact speed using L1 norm."""
        # We want abs(dx) + abs(dy) == speed
        total = abs(self.dx) + abs(self.dy)
        if total == 0:
            return
        self.dx = self.dx * self.speed / total
        self.dy = self.dy * self.speed / total

    def reset(self) -> None:
        """Reset ball to center with random direction."""
        # Position ball in center
        self.x = float(WINDOW_WIDTH / 2 - self.size / 2)
        self.y = float(GAME_AREA_TOP + (GAME_AREA_HEIGHT / 2) - (self.size / 2))

        # Reset speed
        self.speed = float(BALL_SPEED)

        # Set random angle between -45 and 45 degrees
        angle = math.radians(random.uniform(-45, 45))
        # Randomly choose left/right direction
        direction = random.choice([-1, 1])

        # Calculate velocity components to ensure L1 norm equals speed
        # We want |dx| + |dy| = speed
        # For angle A: dx = speed * cos(A), dy = speed * sin(A)
        # Therefore: speed * (|cos(A)| + |sin(A)|) = speed
        # So we need to divide by (|cos(A)| + |sin(A)|)
        norm = abs(math.cos(angle)) + abs(math.sin(angle))
        self.dx = direction * self.speed * math.cos(angle) / norm
        self.dy = self.speed * math.sin(angle) / norm

        # Update collision rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.logger.debug(
            "Ball reset: pos=(%f, %f), vel=(%f, %f), speed=%f",
            self.x,
            self.y,
            self.dx,
            self.dy,
            self.speed,
        )

    def move(self, paddles: List[Paddle]) -> Optional[str]:
        """Move the ball and handle collisions.

        Args:
            paddles: List of paddles to check for collisions

        Returns:
            String indicating scoring ("p1_scored" or "p2_scored") or None
        """
        # Update position
        self.x += self.dx
        self.y += self.dy

        # Update collision rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Check wall collisions
        if self.y <= float(GAME_AREA_TOP):
            self.y = float(GAME_AREA_TOP)
            self.dy = abs(self.dy)  # Bounce down
        elif self.y + self.size >= float(GAME_AREA_TOP + GAME_AREA_HEIGHT):
            self.y = float(GAME_AREA_TOP + GAME_AREA_HEIGHT - self.size)
            self.dy = -abs(self.dy)  # Bounce up

        # Check scoring
        if self.x <= 0:
            self.x = 0.0  # Ensure ball stops at boundary
            return "p2_scored"
        elif self.x + self.size >= float(WINDOW_WIDTH):
            self.x = float(WINDOW_WIDTH - self.size)  # Ensure ball stops at boundary
            return "p1_scored"

        # Check paddle collisions
        for paddle in paddles:
            collision = paddle.get_relative_hit_position(self.rect)
            if collision is not None:
                # Get collision point
                hit_point = paddle.get_collision_point(self.rect)
                if hit_point:
                    # Position ball at collision point
                    if paddle.is_left:
                        self.x = hit_point[0]  # Position at right edge of left paddle
                    else:
                        self.x = hit_point[0] - self.size  # Position at left edge of right paddle
                    self.rect.x = int(self.x)

                    # Increase speed
                    self.speed = min(self.speed + self.speed_increase, self.max_speed)

                    # Calculate new angle based on where ball hit paddle
                    # collision is between -1 (top) and 1 (bottom)
                    angle = math.radians(collision * 45)  # Convert to angle between -45 and 45

                    # Calculate new velocity components with L1 norm normalization
                    norm = abs(math.cos(angle)) + abs(math.sin(angle))
                    if paddle.is_left:
                        # Ball hit left paddle, should move right
                        self.dx = abs(self.speed * math.cos(angle) / norm)
                    else:
                        # Ball hit right paddle, should move left
                        self.dx = -abs(self.speed * math.cos(angle) / norm)
                    self.dy = self.speed * math.sin(angle) / norm

                    self.logger.debug(
                        "Paddle collision: pos=(%f, %f), vel=(%f, %f), speed=%f, angle=%f",
                        self.x,
                        self.y,
                        self.dx,
                        self.dy,
                        self.speed,
                        math.degrees(angle),
                    )

                    break  # Only collide with one paddle per frame

        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the ball on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)
