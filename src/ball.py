"""Ball class for the Pong game."""

import pygame
import math
from .constants import BALL_SIZE, WINDOW_HEIGHT, BALL_SPEED

class Ball:
    """Represents the game ball with position, movement, and collision detection."""
    
    def __init__(self, x, y):
        """Initialize the ball with starting position."""
        self.x = x
        self.y = y
        self.angle = 45  # Starting angle in degrees
        self.velocity = BALL_SPEED
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
    
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
        pygame.draw.rect(screen, (255, 255, 255), self.rect) 