"""Main entry point for the Pong game."""

import sys
import os
from src.game import Game
from src.player import HumanPlayer, AIPlayer, ComputerPlayer
from src.game_state import GameState


def print_usage():
    """Print usage instructions."""
    print("Usage: python main.py [mode] [options]")
    print("Available modes:")
    print("  human-human   : Two human players")
    print("  record-human  : Two human players with gameplay recording")
    print("  human-ai     : Human vs AI")
    print("  human-comp   : Human vs Computer")
    print("  ai-ai        : AI vs AI")
    print("\nOptions:")
    print("  --train N    : Train for N games in headless mode")
    print("  --speed      : Run AI games at maximum speed")
    print("  --fresh      : Start with fresh AI (ignore saved state)")
    print("  --learn      : Learn from recorded human games before starting")


def main():
    """Start and run the game."""
    # Parse game mode and options
    mode = "human-human"  # default mode
    headless = False
    max_games = None
    fresh_start = False
    learn_from_humans = False

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
            if os.path.exists("ai_stats.json"):
                os.remove("ai_stats.json")
        elif arg == "--learn":
            learn_from_humans = True
        elif arg.lower() in ["human-human", "record-human", "human-ai", "human-comp", "comp-comp", "ai-ai"]:
            mode = arg.lower()
        else:
            print(f"Unknown argument: {arg}")
            print_usage()
            return
        i += 1

    # Learn from human games if requested (and not starting fresh)
    if learn_from_humans and not fresh_start:
        # Create temporary AI to learn
        game_state = GameState()
        temp_paddle = None  # Paddle not needed for learning
        ai = AIPlayer(temp_paddle, game_state)
        ai.learn_from_human_games()

    # Set up player types based on mode
    if mode == "human-human":
        game = Game(HumanPlayer, HumanPlayer, headless=headless, record_gameplay=False)
    elif mode == "record-human":
        game = Game(HumanPlayer, HumanPlayer, headless=headless, record_gameplay=True)
    elif mode == "human-ai":
        game = Game(HumanPlayer, AIPlayer, headless=headless, record_gameplay=True)
    elif mode == "human-comp":
        game = Game(HumanPlayer, ComputerPlayer, headless=headless, record_gameplay=False)
    elif mode == "comp-comp":
        game = Game(ComputerPlayer, ComputerPlayer, headless=headless, record_gameplay=False)
    elif mode == "ai-ai":
        game = Game(AIPlayer, AIPlayer, headless=headless, record_gameplay=False)
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
