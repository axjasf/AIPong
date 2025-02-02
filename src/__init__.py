"""Pong game package."""

import logging
import os
from datetime import datetime

from .game import Game
from .ball import Ball
from .paddle import Paddle
from .player import HumanPlayer, ComputerPlayer
from .game_state import GameState

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")


def setup_logging(minimal: bool = False) -> logging.Logger:
    """Configure logging for the application.
    
    Args:
        minimal: If True, only log warnings and errors to file but show game events on screen
    """
    if minimal:
        # Use a single log file for overnight runs
        log_file = "logs/pong_overnight.log"
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        
        # Setup file handler for warnings and errors only
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.WARNING)
        
        # Setup console output for game events
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)  # Show game events but not debug
        
        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)  # Allow all logs to be processed
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        return root_logger
    
    # Normal logging with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/pong_{timestamp}.log"

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Setup file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger


logger = setup_logging()

__all__ = [
    'Game',
    'HumanPlayer',
    'ComputerPlayer',
    'GameState',
]
