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
from typing import Optional, Union

import pygame

from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
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

    # Create game objects
    ball = Ball()
    game_state = GameState()

    # Create paddles
    left_paddle = Paddle(
        PADDLE_WIDTH,
        GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2,
        True
    )
    right_paddle = Paddle(
        WINDOW_WIDTH - 2 * PADDLE_WIDTH,
        GAME_AREA_TOP + (GAME_AREA_HEIGHT - PADDLE_HEIGHT) // 2,
        False
    )

    # Create players
    player1: Union[HumanPlayer, AIPlayer]
    if player1_type == "human":
        player1 = HumanPlayer(left_paddle, P1_UP_KEY, P1_DOWN_KEY)
    else:
        player1 = AIPlayer(left_paddle, game_state)

    player2: Union[HumanPlayer, AIPlayer]
    if player2_type == "human":
        player2 = HumanPlayer(right_paddle, P2_UP_KEY, P2_DOWN_KEY)
    else:
        player2 = AIPlayer(right_paddle, game_state)

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