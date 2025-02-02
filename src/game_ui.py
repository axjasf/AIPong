"""Game UI handling.

This module contains the GameUI class that handles all UI-related functionality:
- Screen initialization
- Drawing game objects
- Rendering scores and text
"""

from typing import List, Optional

import pygame

from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    BLACK,
    WHITE,
    SCORE_COLOR,
    SCORE_FONT_SIZE,
    WINNER_FONT_SIZE,
    SCORE_MARGIN_TOP,
    P1_SCORE_X,
    P2_SCORE_X,
)
from .ball import Ball
from .paddle import Paddle


class GameUI:
    """Handles all UI-related functionality."""

    def __init__(self, headless: bool = False) -> None:
        """Initialize the UI system."""
        self.headless = headless
        self.screen: Optional[pygame.Surface] = None
        self.score_font: Optional[pygame.font.Font] = None
        self.winner_font: Optional[pygame.font.Font] = None

        if not headless:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Pong")
            self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
            self.winner_font = pygame.font.Font(None, WINNER_FONT_SIZE)

    def set_recording_mode(self) -> None:
        """Update caption to indicate recording mode."""
        if not self.headless:
            pygame.display.set_caption("Pong - Recording Gameplay")

    def draw_winner(self, winner: Optional[str]) -> None:
        """Draw the winner announcement."""
        if not winner or self.headless or not self.screen or not self.winner_font:
            return

        text = f"{winner} Wins! Press SPACE for new game"
        winner_text: pygame.Surface = self.winner_font.render(text, True, WHITE)
        winner_rect: pygame.Rect = winner_text.get_rect(
            center=(WINDOW_WIDTH // 2, GAME_AREA_TOP + GAME_AREA_HEIGHT // 2)
        )
        self.screen.blit(winner_text, winner_rect)

    def draw_scores(self, score_p1: int, score_p2: int) -> None:
        """Draw the scores on the screen."""
        if self.headless or not self.screen or not self.score_font:
            return

        # Draw current game scores
        p1_text: pygame.Surface = self.score_font.render(str(score_p1), True, SCORE_COLOR)
        p1_rect: pygame.Rect = p1_text.get_rect(midtop=(P1_SCORE_X, SCORE_MARGIN_TOP))
        self.screen.blit(p1_text, p1_rect)

        p2_text: pygame.Surface = self.score_font.render(str(score_p2), True, SCORE_COLOR)
        p2_rect: pygame.Rect = p2_text.get_rect(midtop=(P2_SCORE_X, SCORE_MARGIN_TOP))
        self.screen.blit(p2_text, p2_rect)

    def draw(
        self,
        ball: Ball,
        paddles: List[Paddle],
        score_p1: int,
        score_p2: int,
        game_over: bool,
        winner: Optional[str],
    ) -> None:
        """Draw all game objects and UI elements.

        Args:
            ball: Ball object to draw
            paddles: List of paddles to draw
            score_p1: Player 1's score
            score_p2: Player 2's score
            game_over: Whether the game is over
            winner: Winner's name if game is over
        """
        if self.headless or not self.screen:
            return

        self.screen.fill(BLACK)

        # Draw game area separator line
        pygame.draw.line(
            self.screen,
            WHITE,
            (0, GAME_AREA_TOP),
            (WINDOW_WIDTH, GAME_AREA_TOP),
        )

        # Draw game objects
        for paddle in paddles:
            paddle.draw(self.screen)
        ball.draw(self.screen)

        # Draw UI elements
        self.draw_scores(score_p1, score_p2)
        if game_over:
            self.draw_winner(winner)

        pygame.display.flip() 