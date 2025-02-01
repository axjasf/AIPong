"""Pong Game Ball Class.

This module contains the Ball class that handles:
- Ball movement and physics
- Collision detection with walls and paddles
- Scoring when ball goes out of bounds
- Ball reset after scoring
"""

from typing import List, Optional
import pygame
import math
import random
from .constants import (
    # Game Objects
    BALL_SIZE, BALL_SPEED, BALL_COLOR,
    
    # Window and Layout
    WINDOW_WIDTH,
    GAME_AREA_TOP, GAME_AREA_HEIGHT
)
from .paddle import Paddle

class Ball:
    """Represents the game ball with position, movement, and collision detection."""
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize the ball with starting position."""
        self.start_x: float = x
        self.start_y: float = y
        self.x: float = x
        self.y: float = y
        self.angle: float = random.uniform(30, 60)  # Random starting angle
        if random.random() < 0.5:  # 50% chance to start towards each player
            self.angle = 180 - self.angle
        self.velocity: float = BALL_SPEED
        self.rect: pygame.Rect = pygame.Rect(int(x), int(y), BALL_SIZE, BALL_SIZE)
    
    def reset(self) -> None:
        """Reset ball to starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.angle = random.uniform(30, 60)
        if random.random() < 0.5:
            self.angle = 180 - self.angle
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def move(self, paddles: List[Paddle]) -> Optional[str]:
        """Update ball position and handle collisions.
        
        Returns:
            Optional[str]: 'p1_scored' if player 1 scored, 'p2_scored' if player 2 scored,
                         None if no scoring occurred.
        """
        # Convert angle to radians for math functions
        rad_angle: float = math.radians(self.angle)
        
        # Calculate new position
        new_x: float = self.x + (self.velocity * math.cos(rad_angle))
        new_y: float = self.y + (self.velocity * math.sin(rad_angle))
        
        # Update rect for collision detection
        self.rect.x = int(new_x)
        self.rect.y = int(new_y)
        
        # Check if ball is out of bounds (scoring)
        if new_x < 0:
            self.reset()
            return "p2_scored"
        elif new_x > WINDOW_WIDTH:
            self.reset()
            return "p1_scored"
        
        # Wall collisions (top and bottom of game area)
        game_area_bottom = GAME_AREA_TOP + GAME_AREA_HEIGHT - BALL_SIZE
        if new_y <= GAME_AREA_TOP or new_y >= game_area_bottom:
            self.angle = -self.angle  # Reflect angle
            # Keep ball within bounds
            if new_y <= GAME_AREA_TOP:
                new_y = GAME_AREA_TOP
            else:
                new_y = game_area_bottom
        
        # Paddle collisions
        for paddle in paddles:
            if self.rect.colliderect(paddle.rect):
                # Add some randomness to the reflection
                self.angle = 180 - self.angle + random.uniform(-10, 10)
                # Ensure angle is not too vertical
                if 80 < self.angle < 100:
                    self.angle = 80 if self.angle < 90 else 100
                elif 260 < self.angle < 280:
                    self.angle = 260 if self.angle < 270 else 280
                break
        
        # Update position
        self.x = new_x
        self.y = new_y
        return None
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the ball on the screen."""
        pygame.draw.rect(screen, BALL_COLOR, self.rect) 