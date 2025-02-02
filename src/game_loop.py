"""Game loop handling.

This module contains the GameLoop class that handles:
- Main game loop
- Game state updates
- Input handling
"""

import logging
import pygame
from typing import Optional, Tuple

from .constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_HEIGHT,
    FPS,
    RESET_DELAY_MS,
)
from .ball import Ball
from .paddle import Paddle
from .player import HumanPlayer, AIPlayer
from .game_state import GameState
from .game_score import GameScore
from .game_recorder import GameRecorder


class GameLoop:
    """Handles the main game loop and updates."""

    def __init__(
        self,
        ball: Ball,
        player1: HumanPlayer | AIPlayer,
        player2: HumanPlayer | AIPlayer,
        game_state: GameState,
        scoring: GameScore,
        recorder: Optional[GameRecorder] = None,
        headless: bool = False,
    ) -> None:
        """Initialize the game loop system."""
        self.logger = logging.getLogger(__name__)
        self.ball = ball
        self.player1 = player1
        self.player2 = player2
        self.game_state = game_state
        self.scoring = scoring
        self.recorder = recorder
        self.headless = headless

        self.clock = pygame.time.Clock()
        self.running = True
        self.waiting_for_reset = False
        self.reset_timer = 0
        self.games_completed = 0
        self.max_games: Optional[int] = None

    def handle_input(self) -> None:
        """Handle keyboard input for game control."""
        if self.headless:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.scoring.game_over:
                    self.reset_game()

    def reset_game(self) -> None:
        """Reset the game state for a new game."""
        self.player1.reset_score()
        self.player2.reset_score()
        self.scoring.reset()
        self.ball.reset()

        # Reset paddle positions to middle
        paddle_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
        self.player1.paddle.set_y(paddle_y)
        self.player2.paddle.set_y(paddle_y)

        self.games_completed += 1

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
            self.running = False

        if self.recorder:
            self.recorder.end_game()
            self.recorder.start_game()

    def update(self) -> None:
        """Update game state."""
        if self.scoring.game_over:
            self.logger.info("Game over. Winner: %s", self.scoring.winner)
            self.reset_game()
            if self.recorder:
                self.recorder.end_game()
                self.recorder.start_game()
            return

        if self.waiting_for_reset:
            current_time = pygame.time.get_ticks()
            if self.headless or current_time - self.reset_timer >= RESET_DELAY_MS:
                self.logger.debug("Resetting ball position")
                self.waiting_for_reset = False
                self.ball.reset()
                self.scoring.reset()
                # Reset paddle positions to middle
                paddle_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
                self.player1.paddle.set_y(paddle_y)
                self.player2.paddle.set_y(paddle_y)
                # Start recording a new point/rally
                if self.recorder:
                    self.recorder.end_game()  # End previous point
                    self.recorder.start_game()  # Start new point
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
            self.scoring.track_hits(left_hit_ball, right_hit_ball)

            # Handle scoring
            if result:
                if self.recorder:
                    # Record who won the point
                    side = "left" if result == "p1_scored" else "right"
                    hits = self.scoring.scores[0] if side == "left" else self.scoring.scores[1]
                    self.recorder.set_winner(side, hits)

                self.scoring.handle_score(self.player1, self.player2, result)
                self.waiting_for_reset = True
                self.reset_timer = pygame.time.get_ticks()

            # Check for game over
            self.scoring.check_winner(self.player1, self.player2)

            # Record frame if in human game
            if self.recorder:
                self.recorder.update_frame(
                    state,
                    self.ball.x,
                    self.ball.y,
                    self.player1.paddle.get_y(),
                    self.player2.paddle.get_y(),
                    left_moved_up,
                    right_moved_up,
                    left_hit_ball,
                    right_hit_ball,
                )

    def run(self, max_games: Optional[int] = None) -> Tuple[Optional[AIPlayer], Optional[AIPlayer]]:
        """Run the main game loop."""
        self.max_games = max_games

        while self.running:
            self.handle_input()

            # In headless mode, update multiple times per frame for speed
            updates_per_frame = 10 if self.headless else 1
            for _ in range(updates_per_frame):
                self.update()

            # Control speed
            if not self.headless:
                self.clock.tick(FPS)

        return (
            self.player1 if isinstance(self.player1, AIPlayer) else None,
            self.player2 if isinstance(self.player2, AIPlayer) else None,
        ) 