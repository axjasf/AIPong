"""Game scoring system.

This module contains the GameScore class that handles:
- Score tracking
- Score display
- Win condition checking
"""

from typing import List, Optional, Tuple, Union

import pygame

from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    SCORE_OFFSET,
    SCORE_COLOR,
    FONT_SIZE,
)


class GameScore:
    """Handles game scoring and display."""

    def __init__(self) -> None:
        """Initialize the scoring system."""
        self.scores = [0, 0]  # [left_score, right_score]
        self.font: Optional[pygame.font.Font] = None

    def reset(self) -> None:
        """Reset scores to zero."""
        self.scores = [0, 0]

    def increment_score(self, is_left_player: bool) -> None:
        """Increment score for the specified player.

        Args:
            is_left_player: Whether to increment left player's score
        """
        if is_left_player:
            self.scores[0] += 1
        else:
            self.scores[1] += 1

    def get_scores(self) -> List[int]:
        """Get current scores.

        Returns:
            List of [left_score, right_score]
        """
        return self.scores.copy()

    def draw(
        self,
        screen: pygame.Surface,
        font: Optional[pygame.font.Font] = None,
    ) -> None:
        """Draw scores on screen.

        Args:
            screen: Surface to draw on
            font: Font to use for rendering (optional)
        """
        # Use provided font or create a new one
        if font:
            self.font = font
        elif not self.font:
            self.font = pygame.font.Font(None, FONT_SIZE)

        # Create score text
        score_text = f"{self.scores[0]}  {self.scores[1]}"
        text_surface = self.font.render(score_text, True, SCORE_COLOR)
        text_rect = text_surface.get_rect(
            centerx=WINDOW_WIDTH // 2,
            top=SCORE_OFFSET,
        )

        # Draw score
        screen.blit(text_surface, text_rect)

    def check_winner(self) -> Optional[int]:
        """Check if there's a winner.

        Returns:
            0 for left player win, 1 for right player win, None if no winner
        """
        if self.scores[0] >= 11 and self.scores[0] - self.scores[1] >= 2:
            return 0
        if self.scores[1] >= 11 and self.scores[1] - self.scores[0] >= 2:
            return 1
        return None 