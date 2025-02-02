# AIPong

A modern implementation of the classic Pong game with AI capabilities, written in Python using Pygame.

[![CI/CD](https://github.com/yourusername/AIPong/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/AIPong/actions/workflows/ci.yml)
[![Code Coverage](https://codecov.io/gh/yourusername/AIPong/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/AIPong)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- Multiple game modes:
  - Human vs Human
  - Human vs AI
  - AI vs AI
  - Training mode
- Neural network-based AI that learns from gameplay
- Record and replay human gameplay for AI training
- Configurable game parameters
- Modern, clean code architecture

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AIPong.git
cd AIPong
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the game with different modes:

```bash
# Human vs Human
python main.py human-human

# Human vs AI
python main.py human-ai

# AI vs AI
python main.py ai-ai

# Train AI
python main.py ai-ai --train 1000 --speed

# Learn from human gameplay
python main.py human-ai --learn
```

### Controls

- Player 1 (Left):
  - W: Move Up
  - S: Move Down

- Player 2 (Right):
  - Up Arrow: Move Up
  - Down Arrow: Move Down

- Space: Start New Game (after game over)

## Development

### Setup Development Environment

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

### Code Quality Tools

- Format code with Black:
```bash
black src/ tests/
```

- Run linting:
```bash
pylint src/ tests/
```

- Run type checking:
```bash
mypy src/ tests/
```

### Running Tests

Run the test suite:
```bash
pytest tests/
```

With coverage:
```bash
pytest --cov=src/ tests/ --cov-report=html
```

### Project Structure

```
AIPong/
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── game.py            # Main game class
│   ├── ball.py            # Ball physics
│   ├── paddle.py          # Paddle controls
│   ├── player.py          # Player implementations
│   ├── game_state.py      # Game state management
│   ├── game_recorder.py   # Gameplay recording
│   └── constants.py       # Game constants
├── tests/                 # Test suite
├── logs/                  # Game logs
├── .github/              # GitHub Actions
├── requirements.txt      # Dependencies
├── pyproject.toml       # Project configuration
├── .pylintrc           # Pylint configuration
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original Pong game by Atari
- Pygame community
- Neural network implementation inspired by modern RL techniques 