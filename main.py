"""Main entry point for the Pong game."""

from src.game import Game

def main():
    """Start and run the game."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()