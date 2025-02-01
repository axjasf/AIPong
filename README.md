# AIPong

A modern implementation of the classic Pong game using Pygame, featuring a modular and maintainable codebase.

## Project Structure

```
AIPong/
├── src/                  # Source code package
│   ├── __init__.py      # Package initialization
│   ├── constants.py     # Game constants and configuration
│   ├── ball.py          # Ball class with physics
│   ├── paddle.py        # Paddle class with controls
│   └── game.py          # Main game logic and loop
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Features
- Two-player gameplay
- Left paddle controlled with W/S keys
- Right paddle controlled with UP/DOWN arrow keys
- Basic physics with angle-based ball movement
- Collision detection for paddles and walls
- Modular code structure for easy maintenance
- Constant configuration for easy tweaking

## Technical Implementation
- **Ball Physics**: Uses trigonometry (sin/cos) for smooth angular movement
- **Collision System**: Utilizes Pygame's rectangle collision detection
- **Game Loop**: Fixed 60 FPS with consistent physics updates
- **Input Handling**: Real-time keyboard input for responsive controls
- **Modular Design**: Separated concerns for better maintainability

## Setup
1. Install Python 3.x
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game
```bash
python main.py
```

## Controls
- Left Paddle:
  - W: Move Up
  - S: Move Down
- Right Paddle:
  - ↑: Move Up
  - ↓: Move Down
- Close window to quit

## Future Enhancements
- Scoring system
- Variable ball reflection angles based on paddle hit position
- Dynamic velocity changes for increased difficulty
- Ball reset mechanism after scoring
- Sound effects and background music
- Menu system and game states
- AI opponent option
- Network multiplayer support

## Contributing
Feel free to fork the repository and submit pull requests for any of the future enhancements or bug fixes.

## License
This project is open source and available under the MIT License. 