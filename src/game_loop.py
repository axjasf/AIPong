"""Game loop handling.

This module contains the GameLoop class that handles:
- Main game loop
- Game state updates
- Input handling
"""

import logging
from typing import Optional, Tuple, Union

import pygame

from .constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_HEIGHT,
    FPS,
    RESET_DELAY_MS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    DIVIDER_COLOR,
    SCORE_OFFSET,
    FONT_SIZE,
    SCORE_COLOR,
    BLACK,
)
from .ball import Ball
from .player import HumanPlayer, AIPlayer
from .game_state import GameState
from .game_score import GameScore


class GameLoop:
    """Handles the main game loop and updates."""

    def __init__(
        self,
        *,  # Force keyword arguments
        ball: Ball,
        player1: Union[HumanPlayer, AIPlayer],
        player2: Union[HumanPlayer, AIPlayer],
        game_state: GameState,
        scoring: GameScore,
        headless: bool = False,
    ) -> None:
        """Initialize the game loop system."""
        self.logger = logging.getLogger(__name__)
        self.ball = ball
        self.player1 = player1
        self.player2 = player2
        self.game_state = game_state
        self.scoring = scoring
        self.headless = headless

        # Initialize display if not headless
        self.screen = None
        if not headless:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Pong")

        self.clock = pygame.time.Clock()
        self.running = True
        self.waiting_for_reset = False
        self.reset_timer = 0
        self.games_completed = 0
        self.max_games: Optional[int] = None
        self.game_over = False
        self.winner: Optional[str] = None

    def handle_input(self) -> None:
        """Handle keyboard input for game control."""
        if self.headless:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()

    def reset_game(self) -> None:
        """Reset the game state for a new game."""
        self.player1.reset_score()
        self.player2.reset_score()
        self.scoring.reset()
        self.ball.reset()
        self.game_over = False
        self.winner = None

        # Reset paddle positions to middle
        paddle_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
        self.player1.paddle.set_y(paddle_y)
        self.player2.paddle.set_y(paddle_y)

        # Stop if we've reached max games
        if self.max_games and self.games_completed >= self.max_games:
            self.running = False

    def update(self) -> None:
        """Update game state."""
        if self.game_over:
            self.logger.info("Game over. Winner: %s", self.winner)
            self.logger.debug("Games completed before reset: %d", self.games_completed)
            self.reset_game()
            self.games_completed += 1
            self.logger.debug("Games completed after increment: %d", self.games_completed)

            # Print only at 10% intervals of total games
            if self.headless and self.max_games:
                milestone = self.max_games // 10
                if self.games_completed % milestone == 0:
                    progress = (self.games_completed * 100) // self.max_games
                    self.logger.info(
                        "Training Progress: %d%% (%d/%d games)",
                        progress,
                        self.games_completed,
                        self.max_games,
                    )

            # Stop if we've reached max games
            if self.max_games and self.games_completed >= self.max_games:
                self.logger.debug("Reached max games (%d), stopping", self.max_games)
                self.running = False
            return

        if self.waiting_for_reset:
            current_time = pygame.time.get_ticks()
            if self.headless or current_time - self.reset_timer >= RESET_DELAY_MS:
                self.logger.debug("Resetting ball position")
                self.waiting_for_reset = False
                self.ball.reset()
                # Reset paddle positions to middle
                paddle_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
                self.player1.paddle.set_y(paddle_y)
                self.player2.paddle.set_y(paddle_y)
        else:
            # Get previous paddle positions for movement detection
            prev_left_y = self.player1.paddle.get_y()
            prev_right_y = self.player2.paddle.get_y()

            # Update game state matrix
            state = self.game_state.update(
                self.ball.x, self.ball.y, self.player1.paddle.get_y(), self.player2.paddle.get_y()
            )

            # Update player paddles
            if not self.waiting_for_reset:
                self.player1.update()
                self.player2.update()

            # Detect paddle movements
            left_moved_up = None
            if self.player1.paddle.get_y() != prev_left_y:
                left_moved_up = self.player1.paddle.get_y() < prev_left_y

            right_moved_up = None
            if self.player2.paddle.get_y() != prev_right_y:
                right_moved_up = self.player2.paddle.get_y() < prev_right_y

            # Update ball and check for scoring
            result = self.ball.move([self.player1.paddle, self.player2.paddle])

            # Track ball hits
            left_hit_ball = self.player1.paddle.rect.colliderect(self.ball.rect)
            right_hit_ball = self.player2.paddle.rect.colliderect(self.ball.rect)

            if left_hit_ball:
                self.game_state.increment_hits(True)
            if right_hit_ball:
                self.game_state.increment_hits(False)

            # Handle scoring
            if result:
                # Update scores
                if result == "p1_scored":
                    self.scoring.increment_score(True)
                    self.player1.increment_score()
                else:
                    self.scoring.increment_score(False)
                    self.player2.increment_score()

                self.waiting_for_reset = True
                self.reset_timer = pygame.time.get_ticks()
                self.game_state.reset_hits()

            # Check for game over
            winner_idx = self.scoring.check_winner()
            if winner_idx is not None:
                self.game_over = True
                self.winner = f"Player {winner_idx + 1}"

                # Handle AI game end
                if isinstance(self.player1, AIPlayer):
                    self.player1.on_game_end(winner_idx == 0)
                if isinstance(self.player2, AIPlayer):
                    self.player2.on_game_end(winner_idx == 1)

    def draw(self) -> None:
        """Draw the game state."""
        if self.headless or not self.screen:
            return

        # Clear screen
        self.screen.fill(BLACK)

        # Draw center line
        pygame.draw.line(
            self.screen,
            DIVIDER_COLOR,
            (WINDOW_WIDTH // 2, GAME_AREA_TOP),
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT),
            1,
        )

        # Draw game objects
        self.ball.draw(self.screen)
        self.player1.paddle.draw(self.screen)
        self.player2.paddle.draw(self.screen)

        # Draw scores
        self.scoring.draw(self.screen)

        # Update display
        pygame.display.flip()

    def run(self, max_games: Optional[int] = None) -> Tuple[Optional[AIPlayer], Optional[AIPlayer]]:
        """Run the main game loop.

        Args:
            max_games: Maximum number of games to play

        Returns:
            Tuple of (player1 if AI, player2 if AI)
        """
        self.max_games = max_games

        # If we start in game over state, handle it immediately
        if self.game_over:
            self.logger.info("Game over. Winner: %s", self.winner)
            self.reset_game()
            self.games_completed += 1
            self.running = False
            return (
                self.player1 if isinstance(self.player1, AIPlayer) else None,
                self.player2 if isinstance(self.player2, AIPlayer) else None,
            )

        while self.running:
            self.handle_input()

            # In headless mode, update multiple times per frame for speed
            updates_per_frame = 10 if self.headless else 1
            for _ in range(updates_per_frame):
                self.update()

            # Draw game state
            self.draw()

            # Control speed
            if not self.headless:
                self.clock.tick(FPS)

        return (
            self.player1 if isinstance(self.player1, AIPlayer) else None,
            self.player2 if isinstance(self.player2, AIPlayer) else None,
        ) 