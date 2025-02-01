"""Pong Game Main Class.

This module contains the main Game class that manages:
- Game initialization and state
- Score tracking
- Player input handling
- Game loop and rendering
- UI elements (header and game area)
"""

import pygame
from typing import List, Optional
from .constants import (
    # Window and Layout
    WINDOW_WIDTH, WINDOW_HEIGHT,
    HEADER_HEIGHT,
    GAME_AREA_TOP, GAME_AREA_HEIGHT,
    
    # Colors
    BLACK, WHITE, SCORE_COLOR,
    
    # Game Rules
    FPS, POINTS_TO_WIN,
    RESET_DELAY_MS,
    
    # Controls
    P1_UP_KEY, P1_DOWN_KEY, P2_UP_KEY, P2_DOWN_KEY,
    
    # UI Elements
    SCORE_FONT_SIZE, WINNER_FONT_SIZE,
    SCORE_MARGIN_TOP, P1_SCORE_X, P2_SCORE_X,
    
    # Game Objects
    LEFT_PADDLE_X, RIGHT_PADDLE_X,
    PADDLE_HEIGHT
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
        
        # Create game objects in the game area
        ball_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2)
        self.ball: Ball = Ball(WINDOW_WIDTH // 2, ball_y)
        
        paddle_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
        self.left_paddle: Paddle = Paddle(LEFT_PADDLE_X, paddle_y, GAME_AREA_TOP, GAME_AREA_TOP + GAME_AREA_HEIGHT)
        self.right_paddle: Paddle = Paddle(RIGHT_PADDLE_X, paddle_y, GAME_AREA_TOP, GAME_AREA_TOP + GAME_AREA_HEIGHT)
        self.paddles: List[Paddle] = [self.left_paddle, self.right_paddle]
        
        # Initialize scores
        self.p1_score: int = 0
        self.p2_score: int = 0
        self.score_font: pygame.font.Font = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.winner_font: pygame.font.Font = pygame.font.Font(None, WINNER_FONT_SIZE)
        
        # Game state
        self.running: bool = True
        self.reset_timer: int = 0
        self.waiting_for_reset: bool = False
        self.game_over: bool = False
        self.winner: Optional[str] = None
    
    def handle_input(self) -> None:
        """Handle keyboard input for paddle movement."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        
        if not self.waiting_for_reset and not self.game_over:
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
    
    def check_winner(self) -> None:
        """Check if either player has won the game."""
        if self.p1_score >= POINTS_TO_WIN:
            self.game_over = True
            self.winner = "Player 1"
        elif self.p2_score >= POINTS_TO_WIN:
            self.game_over = True
            self.winner = "Player 2"
    
    def reset_game(self) -> None:
        """Reset the game state for a new game."""
        self.p1_score = 0
        self.p2_score = 0
        self.game_over = False
        self.winner = None
        self.ball.reset()
    
    def update(self) -> None:
        """Update game state."""
        if self.game_over:
            return
            
        if self.waiting_for_reset:
            if pygame.time.get_ticks() - self.reset_timer >= RESET_DELAY_MS:
                self.waiting_for_reset = False
                self.ball.reset()
        else:
            result = self.ball.move(self.paddles)
            if result == "p1_scored":
                self.p1_score += 1
                self.check_winner()
                self.waiting_for_reset = True
                self.reset_timer = pygame.time.get_ticks()
            elif result == "p2_scored":
                self.p2_score += 1
                self.check_winner()
                self.waiting_for_reset = True
                self.reset_timer = pygame.time.get_ticks()
    
    def draw_winner(self) -> None:
        """Draw the winner announcement."""
        if not self.winner:
            return
            
        text = f"{self.winner} Wins! Press SPACE for new game"
        winner_text: pygame.Surface = self.winner_font.render(text, True, WHITE)
        winner_rect: pygame.Rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, GAME_AREA_TOP + GAME_AREA_HEIGHT // 2))
        self.screen.blit(winner_text, winner_rect)
    
    def draw_scores(self) -> None:
        """Draw the scores on the screen."""
        # Draw current game scores
        p1_text: pygame.Surface = self.score_font.render(str(self.p1_score), True, SCORE_COLOR)
        p1_rect: pygame.Rect = p1_text.get_rect(midtop=(P1_SCORE_X, SCORE_MARGIN_TOP))
        self.screen.blit(p1_text, p1_rect)
        
        p2_text: pygame.Surface = self.score_font.render(str(self.p2_score), True, SCORE_COLOR)
        p2_rect: pygame.Rect = p2_text.get_rect(midtop=(P2_SCORE_X, SCORE_MARGIN_TOP))
        self.screen.blit(p2_text, p2_rect)
    
    def draw(self) -> None:
        """Draw all game objects."""
        self.screen.fill(BLACK)
        
        # Draw game area separator line
        pygame.draw.line(self.screen, WHITE, (0, GAME_AREA_TOP), (WINDOW_WIDTH, GAME_AREA_TOP))
        
        # Draw game objects
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw UI elements
        self.draw_scores()
        if self.game_over:
            self.draw_winner()
        
        pygame.display.flip()
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit() 