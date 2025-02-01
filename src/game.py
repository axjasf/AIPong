"""Main game class for Pong."""

import pygame
from typing import List, Optional
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE,
    LEFT_PADDLE_X, RIGHT_PADDLE_X, FPS,
    P1_UP_KEY, P1_DOWN_KEY, P2_UP_KEY, P2_DOWN_KEY,
    SCORE_FONT_SIZE, SCORE_MARGIN_TOP, P1_SCORE_X, P2_SCORE_X,
    RESET_DELAY_MS
)
from .paddle import Paddle
from .ball import Ball

class Game:
    """Manages the game state and main game loop."""
    
    def __init__(self) -> None:
        """Initialize the game, its objects and pygame."""
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        
        # Create game objects
        self.ball: Ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.left_paddle: Paddle = Paddle(LEFT_PADDLE_X)
        self.right_paddle: Paddle = Paddle(RIGHT_PADDLE_X)
        self.paddles: List[Paddle] = [self.left_paddle, self.right_paddle]
        
        # Initialize scores
        self.p1_score: int = 0
        self.p2_score: int = 0
        self.score_font: pygame.font.Font = pygame.font.Font(None, SCORE_FONT_SIZE)
        
        # Game state
        self.running: bool = True
        self.reset_timer: int = 0
        self.waiting_for_reset: bool = False
    
    def handle_input(self) -> None:
        """Handle keyboard input for paddle movement."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        if not self.waiting_for_reset:
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
    
    def update(self) -> None:
        """Update game state."""
        if self.waiting_for_reset:
            if pygame.time.get_ticks() - self.reset_timer >= RESET_DELAY_MS:
                self.waiting_for_reset = False
                self.ball.reset()
        else:
            result = self.ball.move(self.paddles)
            if result == "p1_scored":
                self.p1_score += 1
                self.waiting_for_reset = True
                self.reset_timer = pygame.time.get_ticks()
            elif result == "p2_scored":
                self.p2_score += 1
                self.waiting_for_reset = True
                self.reset_timer = pygame.time.get_ticks()
    
    def draw_scores(self) -> None:
        """Draw the scores on the screen."""
        # Draw Player 1 score
        p1_text: pygame.Surface = self.score_font.render(str(self.p1_score), True, WHITE)
        p1_rect: pygame.Rect = p1_text.get_rect(midtop=(P1_SCORE_X, SCORE_MARGIN_TOP))
        self.screen.blit(p1_text, p1_rect)
        
        # Draw Player 2 score
        p2_text: pygame.Surface = self.score_font.render(str(self.p2_score), True, WHITE)
        p2_rect: pygame.Rect = p2_text.get_rect(midtop=(P2_SCORE_X, SCORE_MARGIN_TOP))
        self.screen.blit(p2_text, p2_rect)
    
    def draw(self) -> None:
        """Draw all game objects."""
        self.screen.fill(BLACK)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_scores()
        pygame.display.flip()
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit() 