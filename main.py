"""Main entry point for the Pong game."""

import sys
import os
from src.game import Game
from src.player import HumanPlayer, SimpleAIPlayer, ComputerPlayer
from src.game_state import GameState
from src import setup_logging


def print_usage():
    """Print usage instructions."""
    print("Usage: python main.py [mode] [options]")
    print("Available modes:")
    print("  human-human   : Two human players")
    print("  human-ai     : Human vs AI")
    print("  human-comp   : Human vs Computer")
    print("  comp-comp    : Computer vs Computer")
    print("  comp-ai      : Computer vs AI")
    print("  ai-ai        : AI vs AI")
    print("\nOptions:")
    print("  --train N    : Train for N games in headless mode")
    print("  --speed      : Run AI games at maximum speed")
    print("  --fresh      : Start with fresh AI (ignore saved weights)")
    print("  --minimal    : Minimal logging (good for overnight runs)")


def main():
    """Start and run the game."""
    # Parse game mode and options
    mode = "human-human"  # default mode
    headless = False
    max_games = None
    fresh_start = False
    minimal_logging = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--train":
            headless = True
            i += 1
            if i < len(args):
                max_games = int(args[i])
        elif arg == "--speed":
            headless = True
        elif arg == "--fresh":
            fresh_start = True
            if os.path.exists("ai_weights.npy"):
                os.remove("ai_weights.npy")
        elif arg == "--minimal":
            minimal_logging = True
        elif arg.lower() in ["human-human", "human-ai", "human-comp", "comp-comp", "comp-ai", "ai-ai"]:
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
    elif mode == "human-ai":
        game = Game(HumanPlayer, SimpleAIPlayer, headless=headless)
    elif mode == "human-comp":
        game = Game(HumanPlayer, ComputerPlayer, headless=headless)
    elif mode == "comp-comp":
        game = Game(ComputerPlayer, ComputerPlayer, headless=headless)
    elif mode == "comp-ai":
        game = Game(ComputerPlayer, SimpleAIPlayer, headless=headless)
    elif mode == "ai-ai":
        game = Game(SimpleAIPlayer, SimpleAIPlayer, headless=headless)
    else:
        print(f"Unknown mode: {mode}")
        print_usage()
        return

    # Run the game
    if max_games is not None:
        game.run(max_games=max_games)
    else:
        game.run()


if __name__ == "__main__":
    main()
