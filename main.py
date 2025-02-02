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
    print("  --p1         : First player difficulty (easy/normal/hard)")
    print("  --p2         : Second player difficulty (easy/normal/hard)")


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
    p1_difficulty = "normal"  # default difficulty for player 1
    p2_difficulty = "normal"  # default difficulty for player 2

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--speed":
            headless = True
        elif arg == "--minimal":
            minimal_logging = True
        elif arg == "--p1" and i + 1 < len(args):
            p1_difficulty = args[i + 1].lower()
            if p1_difficulty not in ["easy", "normal", "hard"]:
                print(f"Invalid difficulty for player 1: {p1_difficulty}")
                print_usage()
                return
            i += 1
        elif arg == "--p2" and i + 1 < len(args):
            p2_difficulty = args[i + 1].lower()
            if p2_difficulty not in ["easy", "normal", "hard"]:
                print(f"Invalid difficulty for player 2: {p2_difficulty}")
                print_usage()
                return
            i += 1
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
        # Create computer player with specified difficulty
        computer = lambda p: ComputerPlayer(p, difficulty=p2_difficulty)
        game = Game(HumanPlayer, computer, headless=headless)
    elif mode == "comp-comp":
        # Create both computer players with their respective difficulties
        computer1 = lambda p: ComputerPlayer(p, difficulty=p1_difficulty)
        computer2 = lambda p: ComputerPlayer(p, difficulty=p2_difficulty)
        game = Game(computer1, computer2, headless=headless)
    else:
        print(f"Unknown mode: {mode}")
        print_usage()
        return

    # Run the game
    game.run()


if __name__ == "__main__":
    main()
