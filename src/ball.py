"""Ball class for the Pong game."""

from typing import List, Optional
import pygame
import math
from .constants import (
    BALL_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH, 
    BALL_SPEED, BALL_COLOR
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
        self.angle: float = 45  # Starting angle in degrees
        self.velocity: float = BALL_SPEED
        self.rect: pygame.Rect = pygame.Rect(int(x), int(y), BALL_SIZE, BALL_SIZE)
    
    def reset(self) -> None:
        """Reset ball to starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.angle = 45 if self.angle < 180 else 135  # Alternate starting direction
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
        
        # Wall collisions (top and bottom)
        if new_y <= 0 or new_y >= WINDOW_HEIGHT - BALL_SIZE:
            self.angle = -self.angle  # Reflect angle
        
        # Paddle collisions
        for paddle in paddles:
            if self.rect.colliderect(paddle.rect):
                self.angle = 180 - self.angle
                break
        
        # Update position
        self.x = new_x
        self.y = new_y
        return None
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the ball on the screen."""
        pygame.draw.rect(screen, BALL_COLOR, self.rect) 