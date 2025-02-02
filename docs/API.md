# AIPong API Documentation

## Core Classes

### Game

The main game orchestrator that manages the game loop and state.

```python
class Game:
    def __init__(self, player1_type: Type[Player] = HumanPlayer, 
                 player2_type: Type[Player] = HumanPlayer,
                 headless: bool = False,
                 record_gameplay: bool = False) -> None
```

**Parameters:**
- `player1_type`: Class for player 1 (left)
- `player2_type`: Class for player 2 (right)
- `headless`: If True, run without graphics (for training)
- `record_gameplay`: If True, record human gameplay for AI learning

**Methods:**
- `run(max_games: Optional[int] = None) -> Tuple[AIPlayer, AIPlayer]`: Main game loop
- `update() -> None`: Update game state
- `reset_game() -> None`: Reset the game state for a new game

### Player

Abstract base class for all player types.

```python
class Player(ABC):
    def __init__(self, paddle: Paddle)
    
    @abstractmethod
    def update(self) -> None:
        """Update the player's paddle position."""
        pass
```

#### HumanPlayer

Human-controlled player using keyboard input.

```python
class HumanPlayer(Player):
    def __init__(self, paddle: Paddle, up_key: int, down_key: int)
```

#### AIPlayer

AI-controlled player using reinforcement learning.

```python
class AIPlayer(Player):
    def __init__(self, paddle: Paddle, game_state: GameState, 
                 num_nodes: int = 20, learning_rate: float = 0.02)
```

**Methods:**
- `learn(reward: float) -> None`: Update weights based on reward
- `learn_from_human_games() -> None`: Learn from recorded gameplay
- `on_game_end(won: bool) -> None`: Process end of game

### Ball

Handles ball physics and collision detection.

```python
class Ball:
    def __init__(self, x: float, y: float)
    
    def move(self, paddles: List[Paddle]) -> Optional[str]:
        """Update ball position and handle collisions."""
```

**Returns:**
- `"p1_scored"`: if player 1 scored
- `"p2_scored"`: if player 2 scored
- `None`: if no scoring occurred

### GameState

Grid-based state representation for AI input.

```python
class GameState:
    def __init__(self, grid_width: int = 40, grid_height: int = 30)
    
    def update(self, ball_x: float, ball_y: float,
               left_paddle_y: float, right_paddle_y: float) -> np.ndarray:
        """Update the state matrix with new positions."""
```

## Usage Examples

### Creating a Game

```python
# Human vs Human
game = Game(HumanPlayer, HumanPlayer)
game.run()

# Human vs AI
game = Game(HumanPlayer, AIPlayer)
game.run()

# Training AI
game = Game(AIPlayer, AIPlayer, headless=True)
game.run(max_games=1000)
```

### Recording Human Gameplay

```python
# Record a human game
game = Game(HumanPlayer, HumanPlayer, record_gameplay=True)
game.run()

# Train AI from recordings
ai_game = Game(AIPlayer, AIPlayer)
ai_game.player1.learn_from_human_games()
```

## Constants

Game constants are defined in `constants.py`:

```python
# Window and Layout
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
HEADER_HEIGHT = 50
GAME_AREA_TOP = HEADER_HEIGHT
GAME_AREA_HEIGHT = WINDOW_HEIGHT - HEADER_HEIGHT

# Game Rules
FPS = 60
POINTS_TO_WIN = 11
RESET_DELAY_MS = 1000

# Game Objects
BALL_SIZE = 15
BALL_SPEED = 7
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 5
``` 