# AI Pong

A modern implementation of the classic Pong game with AI capabilities, built using Python and Pygame.

## Features

- Classic Pong gameplay with smooth controls and physics
- Multiple game modes:
  - Human vs Human
  - Human vs AI
  - AI vs AI
- AI player with reinforcement learning capabilities
- Headless mode for fast AI training
- Configurable game settings
- Comprehensive logging system

## Requirements

- Python 3.10 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-pong.git
cd ai-pong
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Playing the Game

Run the game with default settings (Human vs Human):
```bash
python -m src.main
```

Available command-line options:
- `--player1`: Type of player 1 (left paddle) - "human" or "ai"
- `--player2`: Type of player 2 (right paddle) - "human" or "ai"
- `--headless`: Run without graphics (for training)
- `--max-games`: Maximum number of games to play

Examples:
```bash
# Human vs AI
python -m src.main --player2 ai

# AI vs AI training
python -m src.main --player1 ai --player2 ai --headless --max-games 1000
```

### Controls

- Player 1 (left):
  - W: Move paddle up
  - S: Move paddle down

- Player 2 (right):
  - Up Arrow: Move paddle up
  - Down Arrow: Move paddle down

- General:
  - Space: Start new game (after game over)
  - ESC: Quit game

## Project Structure

```
ai-pong/
├── src/
│   ├── __init__.py
│   ├── main.py          # Main game entry point
│   ├── ball.py          # Ball physics and movement
│   ├── paddle.py        # Paddle handling
│   ├── player.py        # Player classes (Human/AI)
│   ├── game_state.py    # Game state management
│   ├── game_score.py    # Scoring system
│   ├── game_loop.py     # Main game loop
│   └── constants.py     # Game constants
├── tests/               # Test files
├── models/              # Saved AI models
├── logs/               # Game logs
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project uses:
- Black for code formatting
- Pylint for linting
- Mypy for type checking

Run style checks:
```bash
black src/
pylint src/
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original Pong game by Atari
- Pygame community for the excellent game development library
- TensorFlow team for the machine learning framework 