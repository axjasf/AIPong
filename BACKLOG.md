# Feature Backlog

## Removed Features

### Game Recording System
- Game state recording for AI training
- Components:
  - `src/game_recorder.py`
  - `tests/test_game_recorder.py`
  - Recording-related UI elements
- Command line flag: `--record`
- Training data storage in `training_data/` directory
- Features:
  - Recording game states
  - Recording paddle actions
  - Recording game outcomes
  - Saving training data
  - Loading recorded games

### Integration Points Removed
- Game class recording initialization
- GameLoop recording updates
- UI recording mode indicators
- Documentation references in:
  - README.md
  - docs/API.md

### Future Considerations
- May be reintroduced when AI training capabilities are expanded
- Consider alternative approaches to game state capture
- Potential integration with replay system 