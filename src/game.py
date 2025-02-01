"""Main game class for Pong."""

import pygame
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE,
    LEFT_PADDLE_X, RIGHT_PADDLE_X, FPS,
    P1_UP_KEY, P1_DOWN_KEY, P2_UP_KEY, P2_DOWN_KEY
)
from .paddle import Paddle
from .ball import Ball

class Game:
    """Manages the game state and main game loop."""
    
    def __init__(self):
        """Initialize the game, its objects and pygame."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.left_paddle = Paddle(LEFT_PADDLE_X)
        self.right_paddle = Paddle(RIGHT_PADDLE_X)
        self.paddles = [self.left_paddle, self.right_paddle]
        
        self.running = True
    
    def handle_input(self):
        """Handle keyboard input for paddle movement."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()
        # Player 1 (Left paddle)
        if keys[P1_UP_KEY]:
            self.left_paddle.move(up=True)
        if keys[P1_DOWN_KEY]:
            self.left_paddle.move(up=False)
            
        # Player 2 (Right paddle)
        if keys[P2_UP_KEY]:
            self.right_paddle.move(up=True)
        if keys[P2_DOWN_KEY]:
            self.right_paddle.move(up=False)
    
    def update(self):
        """Update game state."""
        self.ball.move(self.paddles)
    
    def draw(self):
        """Draw all game objects."""
        self.screen.fill(BLACK)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit() 