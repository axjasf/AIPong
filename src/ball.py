"""Ball class for the Pong game."""

import pygame
import math
from .constants import (
    BALL_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH, 
    BALL_SPEED, BALL_COLOR
)

class Ball:
    """Represents the game ball with position, movement, and collision detection."""
    
    def __init__(self, x, y):
        """Initialize the ball with starting position."""
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.angle = 45  # Starting angle in degrees
        self.velocity = BALL_SPEED
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
    
    def reset(self):
        """Reset ball to starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.angle = 45 if self.angle < 180 else 135  # Alternate starting direction
        self.rect.x = self.x
        self.rect.y = self.y
    
    def move(self, paddles):
        """Update ball position and handle collisions."""
        # Convert angle to radians for math functions
        rad_angle = math.radians(self.angle)
        
        # Calculate new position
        new_x = self.x + (self.velocity * math.cos(rad_angle))
        new_y = self.y + (self.velocity * math.sin(rad_angle))
        
        # Update rect for collision detection
        self.rect.x = int(new_x)
        self.rect.y = int(new_y)
        
        # Check if ball is out of bounds
        if new_x < 0 or new_x > WINDOW_WIDTH:
            self.reset()
            return
        
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
    
    def draw(self, screen):
        """Draw the ball on the screen."""
        pygame.draw.rect(screen, BALL_COLOR, self.rect) 