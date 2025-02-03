"""Pong Game Main Class.

This module contains the main Game class that manages:
- Game initialization and state
- Score tracking
- Game loop and rendering
- UI elements (header and game area)
"""

import logging
import os
from typing import List, Optional, Type, Tuple, Union, TypeVar, Callable

import pygame

from .constants import (
    # Window and Layout
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    GAME_AREA_WIDTH,
    # Colors
    BLACK,
    WHITE,
    SCORE_COLOR,
    # Game Rules
    FPS,
    POINTS_TO_WIN,
    RESET_DELAY_MS,
    # Controls
    P1_UP_KEY,
    P1_DOWN_KEY,
    P2_UP_KEY,
    P2_DOWN_KEY,
    # UI Elements
    SCORE_FONT_SIZE,
    WINNER_FONT_SIZE,
    SCORE_MARGIN_TOP,
    P1_SCORE_X,
    P2_SCORE_X,
    # Game Objects
    PADDLE_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_MARGIN,
    BALL_SIZE,
)
from .paddle import Paddle
from .ball import Ball
from .player import HumanPlayer, AIPlayer, ComputerPlayer, Player
from .game_state import GameState


# Type variable for player types
P = TypeVar("P", bound=Player)


class Game:
    """Manages the game state and main game loop."""

    def __init__(
        self,
        player1_type: Union[Type[P], Callable[[Paddle], P]] = HumanPlayer,
        player2_type: Union[Type[P], Callable[[Paddle], P]] = HumanPlayer,
        headless: bool = False,
    ) -> None:
        """Initialize the game, its objects and pygame."""
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            "Initializing game with players: %s vs %s", 
            getattr(player1_type, "__name__", player1_type.__class__.__name__),
            getattr(player2_type, "__name__", player2_type.__class__.__name__)
        )

        self.headless = headless
        # Initialize screen as None first
        self.screen: Optional[pygame.Surface] = None

        if headless:
            self.logger.debug("Running in headless mode")
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            pygame.init()
        else:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Pong")

        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Create game objects in the game area
        self._init_game_objects()

        # Initialize game state for AI
        self.game_state = GameState()
        self.logger.debug("Game state initialized")

        # Create players based on type
        self.player1: P
        self.player2: P

        # Initialize player 1
        if callable(player1_type) and player1_type != HumanPlayer:
            self.player1 = player1_type(self.paddle_p1)
        elif player1_type == HumanPlayer and not headless:
            self.player1 = HumanPlayer(self.paddle_p1, P1_UP_KEY, P1_DOWN_KEY)
        elif player1_type == ComputerPlayer:
            self.player1 = ComputerPlayer(self.paddle_p1)
            self.player1.ball = self.ball  # Pass ball reference
        else:
            # Ensure we're using AIPlayer
            if not issubclass(player1_type, AIPlayer):
                raise TypeError(
                    "Non-headless mode requires HumanPlayer, ComputerPlayer, or AIPlayer"
                )
            self.player1 = player1_type(self.paddle_p1, self.game_state)

        # Initialize player 2
        if callable(player2_type) and player2_type != HumanPlayer:
            self.player2 = player2_type(self.paddle_p2)
        elif player2_type == HumanPlayer and not headless:
            self.player2 = HumanPlayer(self.paddle_p2, P2_UP_KEY, P2_DOWN_KEY)
        elif player2_type == ComputerPlayer:
            self.player2 = ComputerPlayer(self.paddle_p2)
            self.player2.ball = self.ball  # Pass ball reference
        else:
            # Ensure we're using AIPlayer
            if not issubclass(player2_type, AIPlayer):
                raise TypeError(
                    "Non-headless mode requires HumanPlayer, ComputerPlayer, or AIPlayer"
                )
            self.player2 = player2_type(self.paddle_p2, self.game_state)

        # Set ball reference for computer players
        if isinstance(self.player1, ComputerPlayer):
            self.player1.ball = self.ball
        if isinstance(self.player2, ComputerPlayer):
            self.player2.ball = self.ball

        self.paddles: List[Paddle] = [self.player1.paddle, self.player2.paddle]

        # Initialize fonts if not headless
        if not headless:
            self.score_font: Optional[pygame.font.Font] = pygame.font.Font(None, SCORE_FONT_SIZE)
            self.winner_font: Optional[pygame.font.Font] = pygame.font.Font(None, WINNER_FONT_SIZE)
        else:
            self.score_font = None
            self.winner_font = None

        # Game state
        self.running: bool = True
        self.reset_timer: int = 0
        self.waiting_for_reset: bool = False
        self.game_over: bool = False
        self.winner: Optional[str] = None
        self.is_paused: bool = False
        self.left_hits_this_point: int = 0
        self.right_hits_this_point: int = 0

        # Training stats
        self.games_completed: int = 0
        self.max_games: Optional[int] = None

        self.logger.info("Players initialized successfully")

    def _init_game_objects(self) -> None:
        """Initialize game objects (paddles and ball)."""
        # Initialize paddles
        paddle_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2
        self.paddle_p1 = Paddle(PADDLE_MARGIN, paddle_y, True)  # Left paddle
        self.paddle_p2 = Paddle(
            WINDOW_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH, paddle_y, False
        )  # Right paddle

        # Initialize ball
        self.ball = Ball()

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

    def check_winner(self) -> None:
        """Check if either player has won the game."""
        if self.player1.score >= POINTS_TO_WIN:
            self.game_over = True
            self.winner = "Player 1"
            if isinstance(self.player1, AIPlayer):
                # Only reward if they hit the ball at least twice
                if self.left_hits_this_point >= 2:
                    self.player1.on_game_end(True)
                else:
                    self.player1.on_game_end(False)
            if isinstance(self.player2, AIPlayer):
                self.player2.on_game_end(False)
        elif self.player2.score >= POINTS_TO_WIN:
            self.game_over = True
            self.winner = "Player 2"
            if isinstance(self.player1, AIPlayer):
                self.player1.on_game_end(False)
            if isinstance(self.player2, AIPlayer):
                # Only reward if they hit the ball at least twice
                if self.right_hits_this_point >= 2:
                    self.player2.on_game_end(True)
                else:
                    self.player2.on_game_end(False)

    def reset_game(self) -> None:
        """Reset the game state for a new game."""
        self.player1.reset_score()
        self.player2.reset_score()
        self.game_over = False
        self.winner = None
        self.ball.reset()

        # Reset paddle positions to middle
        paddle_y = GAME_AREA_TOP + (GAME_AREA_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
        self.player1.paddle.set_y(paddle_y)
        self.player2.paddle.set_y(paddle_y)

        # Update ball reference for computer players
        if isinstance(self.player1, ComputerPlayer):
            self.player1.ball = self.ball
            self.player1.last_ball_y = self.ball.y
        if isinstance(self.player2, ComputerPlayer):
            self.player2.ball = self.ball
            self.player2.last_ball_y = self.ball.y

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

    def toggle_pause(self) -> None:
        """Toggle the game's pause state."""
        self.is_paused = not self.is_paused

    def update(self) -> None:
        """Update game state."""
        if self.game_over:
            self.logger.info("Game over. Winner: %s", self.winner)
            self.reset_game()
            return

        if self.is_paused:
            return

        if self.waiting_for_reset:
            current_time = pygame.time.get_ticks()
            if self.headless or current_time - self.reset_timer >= RESET_DELAY_MS:
                self.logger.debug("Resetting ball position")
                self.waiting_for_reset = False
                self.ball.reset()
                self.left_hits_this_point = 0
                self.right_hits_this_point = 0
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

            # Check for paddle collisions before moving ball
            left_hit_ball = self.player1.paddle.rect.colliderect(self.ball.rect)
            right_hit_ball = self.player2.paddle.rect.colliderect(self.ball.rect)

            # Update ball and check for scoring
            result = self.ball.move(self.paddles)

            # Track ball hits after ball movement
            if left_hit_ball:
                self.left_hits_this_point += 1
                self.game_state.left_hits = self.left_hits_this_point
            if right_hit_ball:
                self.right_hits_this_point += 1
                self.game_state.right_hits = self.right_hits_this_point

            if result == "p1_scored":
                self.player1.increment_score()
                self.logger.info(
                    "Player 1 scored. Score: %d-%d", self.player1.score, self.player2.score
                )
                self.waiting_for_reset = True
                self.reset_timer = pygame.time.get_ticks()
            elif result == "p2_scored":
                self.player2.increment_score()
                self.logger.info(
                    "Player 2 scored. Score: %d-%d", self.player1.score, self.player2.score
                )
                self.waiting_for_reset = True
                self.reset_timer = pygame.time.get_ticks()

            # Check for game over
            if self.player1.score >= POINTS_TO_WIN:
                self.logger.info("Player 1 wins the game!")
                self.game_over = True
                self.winner = "Player 1"
            elif self.player2.score >= POINTS_TO_WIN:
                self.logger.info("Player 2 wins the game!")
                self.game_over = True
                self.winner = "Player 2"

    def draw_winner(self) -> None:
        """Draw the winner announcement."""
        if not self.winner or self.headless or not self.screen or not self.winner_font:
            return

        text = f"{self.winner} Wins! Press SPACE for new game"
        winner_text: pygame.Surface = self.winner_font.render(text, True, WHITE)
        winner_rect: pygame.Rect = winner_text.get_rect(
            center=(WINDOW_WIDTH // 2, GAME_AREA_TOP + GAME_AREA_HEIGHT // 2)
        )
        self.screen.blit(winner_text, winner_rect)

    def draw_scores(self) -> None:
        """Draw the scores on the screen."""
        if self.headless or not self.screen or not self.score_font:
            return

        # Draw current game scores
        p1_text: pygame.Surface = self.score_font.render(str(self.player1.score), True, SCORE_COLOR)
        p1_rect: pygame.Rect = p1_text.get_rect(midtop=(P1_SCORE_X, SCORE_MARGIN_TOP))
        self.screen.blit(p1_text, p1_rect)

        p2_text: pygame.Surface = self.score_font.render(str(self.player2.score), True, SCORE_COLOR)
        p2_rect: pygame.Rect = p2_text.get_rect(midtop=(P2_SCORE_X, SCORE_MARGIN_TOP))
        self.screen.blit(p2_text, p2_rect)

    def draw(self) -> None:
        """Draw all game objects."""
        if self.headless or not self.screen:
            return

        self.screen.fill(BLACK)

        # Draw game area separator line
        pygame.draw.line(self.screen, WHITE, (0, GAME_AREA_TOP), (WINDOW_WIDTH, GAME_AREA_TOP))

        # Draw game objects
        self.player1.paddle.draw(self.screen)
        self.player2.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        # Draw UI elements
        self.draw_scores()
        if self.game_over:
            self.draw_winner()

        pygame.display.flip()

    def run(self, max_games: Optional[int] = None) -> Tuple[Optional[AIPlayer], Optional[AIPlayer]]:
        """Main game loop."""
        self.max_games = max_games

        while self.running:
            self.handle_input()

            # In headless mode, update multiple times per frame for speed
            updates_per_frame = 10 if self.headless else 1
            for _ in range(updates_per_frame):
                self.update()

            self.draw()

            # Control speed
            if not self.headless:
                self.clock.tick(FPS)

        if not self.headless:
            pygame.quit()

        return (
            self.player1 if isinstance(self.player1, AIPlayer) else None,
            self.player2 if isinstance(self.player2, AIPlayer) else None,
        )

    @property
    def score(self) -> Tuple[int, int]:
        """Get the current game score.
        
        Returns:
            Tuple of (player1 score, player2 score)
        """
        return (self.player1.score, self.player2.score)
