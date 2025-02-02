"""Main entry point for the Pong game."""

import sys
import os
from typing import Optional, Literal

from src.game import Game
from src.player import HumanPlayer, ComputerPlayer
from src.game_state import GameState
from src import setup_logging


def print_usage():
    """Print usage instructions."""
    print("Usage: python main.py [mode] [options]")
    print("Available modes:")
    print("  human-human   : Two human players")
    print("  human-comp   : Human vs Computer")
    print("  comp-comp    : Computer vs Computer")
    print("\nOptions:")
    print("  --speed      : Run games at maximum speed")
    print("  --minimal    : Minimal logging (good for overnight runs)")
    print("  --easy       : Easy computer opponent (50-200ms reaction)")
    print("  --normal     : Normal computer opponent (30-50ms reaction)")
    print("  --hard       : Hard computer opponent (0-30ms reaction)")


def create_computer_player(paddle, difficulty: Optional[str] = None) -> ComputerPlayer:
    """Create a computer player with the specified difficulty.
    
    Args:
        paddle: The paddle for the player
        difficulty: Optional difficulty setting
        
    Returns:
        ComputerPlayer instance
    """
    if difficulty in ["easy", "normal", "hard"]:
        return ComputerPlayer(paddle, difficulty=difficulty)
    return ComputerPlayer(paddle, difficulty="normal")


def main():
    """Start and run the game."""
    # Parse game mode and options
    mode = "human-human"  # default mode
    headless = False
    minimal_logging = False
    difficulty: Optional[str] = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--speed":
            headless = True
        elif arg == "--minimal":
            minimal_logging = True
        elif arg == "--easy":
            difficulty = "easy"
        elif arg == "--normal":
            difficulty = "normal"
        elif arg == "--hard":
            difficulty = "hard"
        elif arg.lower() in ["human-human", "human-comp", "comp-comp"]:
            mode = arg.lower()
        else:
            print(f"Unknown argument: {arg}")
            print_usage()
            return
        i += 1

    # Setup logging
    setup_logging(minimal=minimal_logging)

    # Set up player types based on mode
    if mode == "human-human":
        game = Game(HumanPlayer, HumanPlayer, headless=headless)
    elif mode == "human-comp":
        game = Game(HumanPlayer, ComputerPlayer, headless=headless)
        # Set difficulty for computer player after initialization
        if isinstance(game.player2, ComputerPlayer):
            game.player2.reaction_delay = game.player2.DELAY_RANGES[difficulty or "normal"][0]
    elif mode == "comp-comp":
        game = Game(ComputerPlayer, ComputerPlayer, headless=headless)
        # Set difficulty for both computer players
        if isinstance(game.player1, ComputerPlayer):
            game.player1.reaction_delay = game.player1.DELAY_RANGES[difficulty or "normal"][0]
        if isinstance(game.player2, ComputerPlayer):
            game.player2.reaction_delay = game.player2.DELAY_RANGES[difficulty or "normal"][0]
    else:
        print(f"Unknown mode: {mode}")
        print_usage()
        return

    # Run the game
    game.run()


if __name__ == "__main__":
    main()
