"""Game scoring system.

This module contains the GameScore class that handles:
- Score tracking
- Game over conditions
- Winner determination
"""

import logging
from typing import Optional, Tuple

from .player import HumanPlayer, AIPlayer


class GameScore:
    """Handles game scoring and win conditions."""

    def __init__(self, points_to_win: int = 11, win_by_two: bool = True) -> None:
        """Initialize the scoring system.

        Args:
            points_to_win: Number of points needed to win (default: 11)
            win_by_two: Whether player needs to win by 2 points (default: True)
        """
        self.logger = logging.getLogger(__name__)
        self.points_to_win = points_to_win
        self.win_by_two = win_by_two
        self.scores = [0, 0]  # [left_score, right_score]
        self.hits = [0, 0]  # [left_hits, right_hits]
        self.game_over = False
        self.winner: Optional[str] = None

    def reset(self) -> None:
        """Reset the hits counter for a new point."""
        self.hits = [0, 0]

    def track_hits(self, left_hit: bool, right_hit: bool) -> None:
        """Track paddle hits for the current point/rally."""
        if left_hit:
            self.hits[0] += 1
        if right_hit:
            self.hits[1] += 1

    def handle_score(
        self, player1: HumanPlayer | AIPlayer, player2: HumanPlayer | AIPlayer, result: str
    ) -> None:
        """Handle scoring based on game result.

        Args:
            player1: Left player
            player2: Right player
            result: Game result ("p1_scored" or "p2_scored")
        """
        if result == "p1_scored":
            self.scores[0] += 1
            player1.increment_score()
            self.logger.info(
                "Player 1 scored! Score: %d-%d (hits: %d-%d)",
                self.scores[0],
                self.scores[1],
                self.hits[0],
                self.hits[1],
            )
        elif result == "p2_scored":
            self.scores[1] += 1
            player2.increment_score()
            self.logger.info(
                "Player 2 scored! Score: %d-%d (hits: %d-%d)",
                self.scores[0],
                self.scores[1],
                self.hits[0],
                self.hits[1],
            )

    def check_winner(self, player1: HumanPlayer | AIPlayer, player2: HumanPlayer | AIPlayer) -> None:
        """Check if there's a winner based on current scores.

        Args:
            player1: Left player
            player2: Right player
        """
        # Get current scores
        p1_score = self.scores[0]
        p2_score = self.scores[1]

        # Check if either player has reached minimum points to win
        if p1_score >= self.points_to_win or p2_score >= self.points_to_win:
            # If win by two is required, check point difference
            if not self.win_by_two or abs(p1_score - p2_score) >= 2:
                self.game_over = True
                if p1_score > p2_score:
                    self.winner = "Player 1"
                else:
                    self.winner = "Player 2"

    def get_scores(self) -> Tuple[int, int]:
        """Get current scores.

        Returns:
            Tuple of (left_score, right_score)
        """
        return tuple(self.scores)  # type: ignore 