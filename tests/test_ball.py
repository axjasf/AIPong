"""Test suite for ball physics and collision detection."""

import unittest
import pygame
import math
from src.ball import Ball
from src.paddle import Paddle
from src.constants import (
    WINDOW_WIDTH, GAME_AREA_TOP,
    GAME_AREA_HEIGHT, BALL_SIZE,
    BALL_SPEED
)

class TestBall(unittest.TestCase):
    """Test cases for Ball class."""
    
    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.start_x = WINDOW_WIDTH // 2
        self.start_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2)
        self.ball = Ball(self.start_x, self.start_y)
        
    def test_ball_initialization(self):
        """Test ball is initialized with correct position and properties."""
        self.assertEqual(self.ball.x, self.start_x)
        self.assertEqual(self.ball.y, self.start_y)
        self.assertEqual(self.ball.rect.width, BALL_SIZE)
        self.assertEqual(self.ball.rect.height, BALL_SIZE)
        self.assertEqual(self.ball.velocity, BALL_SPEED)
        
    def test_ball_reset(self):
        """Test ball reset returns to starting position."""
        # Move ball
        self.ball.x = 100
        self.ball.y = 100
        
        # Reset
        self.ball.reset()
        
        # Check position
        self.assertEqual(self.ball.x, self.start_x)
        self.assertEqual(self.ball.y, self.start_y)
        
    def test_wall_collision(self):
        """Test ball bounces off top and bottom walls."""
        # Move ball to top wall
        self.ball.angle = -45  # Moving up
        self.ball.y = GAME_AREA_TOP + 1
        
        # Update
        self.ball.move([])
        
        # Should bounce down
        self.assertTrue(math.sin(math.radians(self.ball.angle)) > 0)
        
        # Move ball to bottom wall
        self.ball.angle = 45  # Moving down
        self.ball.y = GAME_AREA_TOP + GAME_AREA_HEIGHT - BALL_SIZE - 1
        
        # Update
        self.ball.move([])
        
        # Should bounce up
        self.assertTrue(math.sin(math.radians(self.ball.angle)) < 0)
        
    def test_paddle_collision(self):
        """Test ball bounces off paddles."""
        # Create test paddle
        paddle = Paddle(100, self.start_y, GAME_AREA_TOP, GAME_AREA_TOP + GAME_AREA_HEIGHT)
        
        # Position ball for collision
        self.ball.x = paddle.rect.right + BALL_SIZE
        self.ball.y = paddle.rect.centery
        self.ball.angle = 180  # Moving left
        
        # Update
        self.ball.move([paddle])
        
        # Should bounce right
        self.assertTrue(math.cos(math.radians(self.ball.angle)) > 0)
        
    def test_scoring(self):
        """Test scoring when ball goes out of bounds."""
        # Move ball past left boundary
        self.ball.x = -1
        result = self.ball.move([])
        self.assertEqual(result, "p2_scored")
        
        # Move ball past right boundary
        self.ball.x = WINDOW_WIDTH + 1
        result = self.ball.move([])
        self.assertEqual(result, "p1_scored")

if __name__ == '__main__':
    unittest.main() 