"""Main game module.

This module contains the main game loop and initialization:
- Game setup and configuration
- Window creation
- Game state initialization
- Main loop execution
"""

import argparse
import logging
import os
import pygame
import sys
from typing import Optional, Tuple

from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GAME_AREA_TOP,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    P1_UP_KEY,
    P1_DOWN_KEY,
    P2_UP_KEY,
    P2_DOWN_KEY,
    BLACK,
    DIVIDER_COLOR,
    FONT_SIZE,
    SCORE_OFFSET,
    SCORE_COLOR,
    LOG_DIR,
)
from .ball import Ball
from .paddle import Paddle
from .player import HumanPlayer, AIPlayer
from .game_state import GameState
from .game_score import GameScore
from .game_loop import GameLoop
from .game_recorder import GameRecorder


def setup_logging(log_dir: str = LOG_DIR) -> None:
    """Set up logging configuration.

    Args:
        log_dir: Directory to store log files
    """
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "game.log")),
            logging.StreamHandler(),
        ],
    )


def init_pygame() -> Tuple[pygame.Surface, pygame.font.Font]:
    """Initialize Pygame and create window.

    Returns:
        Tuple of (screen surface, font)
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pong")
    font = pygame.font.Font(None, FONT_SIZE)
    return screen, font


def draw_game(
    screen: pygame.Surface,
    font: pygame.font.Font,
    ball: Ball,
    player1: HumanPlayer | AIPlayer,
    player2: HumanPlayer | AIPlayer,
    scoring: GameScore,
) -> None:
    """Draw the game state.

    Args:
        screen: Pygame surface to draw on
        font: Font for rendering text
        ball: Ball object
        player1: Left player
        player2: Right player
        scoring: Scoring system
    """
    # Clear screen
    screen.fill(BLACK)

    # Draw center line
    pygame.draw.line(
        screen,
        DIVIDER_COLOR,
        (WINDOW_WIDTH // 2, GAME_AREA_TOP),
        (WINDOW_WIDTH // 2, WINDOW_HEIGHT),
        1,
    )

    # Draw scores
    scores = scoring.get_scores()
    score_text = f"{scores[0]}  {scores[1]}"
    text_surface = font.render(score_text, True, SCORE_COLOR)
    text_rect = text_surface.get_rect(
        centerx=WINDOW_WIDTH // 2, top=SCORE_OFFSET
    )
    screen.blit(text_surface, text_rect)

    # Draw game objects
    ball.draw(screen)
    player1.paddle.draw(screen)
    player2.paddle.draw(screen)

    # Update display
    pygame.display.flip()


def main(
    player1_type: str = "human",
    player2_type: str = "human",
    headless: bool = False,
    record_game: bool = False,
    max_games: Optional[int] = None,
) -> None:
    """Run the main game loop.

    Args:
        player1_type: Type of left player ("human" or "ai")
        player2_type: Type of right player ("human" or "ai")
        headless: Whether to run without graphics
        record_game: Whether to record game states
        max_games: Maximum number of games to play
    """
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Pong game")

    # Initialize display if not headless
    screen = None
    font = None
    if not headless:
        screen, font = init_pygame()

    # Create game objects
    ball = Ball()
    game_state = GameState()

    # Create paddles
    left_paddle = Paddle(PADDLE_WIDTH, GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2)
    right_paddle = Paddle(
        WINDOW_WIDTH - 2 * PADDLE_WIDTH,
        GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2,
        is_left=False,
    )

    # Create players
    player1: HumanPlayer | AIPlayer
    if player1_type == "human":
        player1 = HumanPlayer(left_paddle, P1_UP_KEY, P1_DOWN_KEY)
    else:
        player1 = AIPlayer(left_paddle)

    player2: HumanPlayer | AIPlayer
    if player2_type == "human":
        player2 = HumanPlayer(right_paddle, P2_UP_KEY, P2_DOWN_KEY)
    else:
        player2 = AIPlayer(right_paddle)

    # Create scoring system
    scoring = GameScore()

    # Create recorder if needed
    recorder = GameRecorder() if record_game else None

    # Create game loop
    game_loop = GameLoop(
        ball=ball,
        player1=player1,
        player2=player2,
        game_state=game_state,
        scoring=scoring,
        recorder=recorder,
        headless=headless,
    )

    # Start recording if enabled
    if recorder:
        recorder.start_game()

    try:
        # Run game loop
        trained_models = game_loop.run(max_games=max_games)

        # Save trained AI models if any
        if trained_models[0]:
            logger.info("Saving player 1 model")
            trained_models[0].save_model("player1_model")
        if trained_models[1]:
            logger.info("Saving player 2 model")
            trained_models[1].save_model("player2_model")

    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
    finally:
        if recorder:
            recorder.save_games()
        pygame.quit()
        logger.info("Game ended")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pong Game")
    parser.add_argument(
        "--player1",
        choices=["human", "ai"],
        default="human",
        help="Type of player 1 (left paddle)",
    )
    parser.add_argument(
        "--player2",
        choices=["human", "ai"],
        default="human",
        help="Type of player 2 (right paddle)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without graphics (for training)",
    )
    parser.add_argument(
        "--record",
        action="store_true",
        help="Record game states for training",
    )
    parser.add_argument(
        "--max-games",
        type=int,
        help="Maximum number of games to play",
    )

    args = parser.parse_args()
    main(
        player1_type=args.player1,
        player2_type=args.player2,
        headless=args.headless,
        record_game=args.record,
        max_games=args.max_games,
    ) 