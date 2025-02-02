"""Pong game package."""

import logging
import os
from datetime import datetime

from .game import Game
from .ball import Ball
from .paddle import Paddle
from .player import Player, HumanPlayer

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")


# Configure logging
def setup_logging():
    """Configure logging for the application."""
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
