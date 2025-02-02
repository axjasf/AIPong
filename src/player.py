"""Player handling system.

This module contains the base Player class and its implementations:
- HumanPlayer: Handles human input
- AIPlayer: Handles AI decision making
"""

import logging
import json
import os
import numpy as np
import pygame
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from .paddle import Paddle
from .game_state import GameState
from .constants import (
    GAME_AREA_TOP,
    GAME_AREA_HEIGHT,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
)


class Player(ABC):
    """Abstract base class for players."""

    def __init__(self, paddle: Paddle) -> None:
        """Initialize the player.

        Args:
            paddle: The player's paddle
        """
        self.logger = logging.getLogger(__name__)
        self.paddle = paddle
        self.score = 0

    @abstractmethod
    def update(self) -> None:
        """Update the player's paddle position."""
        pass

    def increment_score(self) -> None:
        """Increment the player's score."""
        self.score += 1

    def reset_score(self) -> None:
        """Reset the player's score."""
        self.score = 0


class HumanPlayer(Player):
    """Human player controlled by keyboard input."""

    def __init__(self, paddle: Paddle, up_key: int, down_key: int) -> None:
        """Initialize the human player.

        Args:
            paddle: The player's paddle
            up_key: Pygame key code for moving up
            down_key: Pygame key code for moving down
        """
        super().__init__(paddle)
        self.up_key = up_key
        self.down_key = down_key

    def update(self) -> None:
        """Update paddle position based on keyboard input."""
        keys = pygame.key.get_pressed()

        # Move paddle up/down based on key presses
        if keys[self.up_key]:
            new_y = self.paddle.get_y() - PADDLE_SPEED
            # Ensure paddle stays within game area
            if new_y >= GAME_AREA_TOP:
                self.paddle.set_y(new_y)
        elif keys[self.down_key]:
            new_y = self.paddle.get_y() + PADDLE_SPEED
            # Ensure paddle stays within game area
            if new_y + PADDLE_HEIGHT <= GAME_AREA_TOP + GAME_AREA_HEIGHT:
                self.paddle.set_y(new_y)


class AIPlayer(Player):
    """AI player that makes decisions based on game state."""

    def __init__(
        self,
        paddle: Paddle,
        game_state: GameState,
        num_nodes: int = 20,
        learning_rate: float = 0.02,
    ) -> None:
        """Initialize the AI player."""
        super().__init__(paddle)
        self.game_state = game_state
        self.num_nodes = num_nodes
        self.learning_rate = learning_rate

        # File paths for persistence
        self.weights_file = "ai_weights.npy"
        self.stats_file = "ai_stats.json"

        # Initialize or load weights
        total_inputs = game_state.grid_width * game_state.grid_height
        if os.path.exists(self.weights_file):
            self.weights = np.load(self.weights_file)
        else:
            # Initialize weights for hidden layer with better scaling
            self.weights = np.random.randn(total_inputs, num_nodes) * np.sqrt(2.0 / total_inputs)

        # Training data for learning
        self.last_state: Optional[np.ndarray] = None
        self.last_action: Optional[bool] = None
        self.last_probability: Optional[float] = None

        # Initialize training statistics
        self.games_played: int = 0
        self.total_reward: float = 0

        # Load statistics if available
        if os.path.exists(self.stats_file):
            with open(self.stats_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
                # Update without type annotations since they're already defined
                self.games_played = int(stats["games_played"])  # Ensure type safety
                self.total_reward = float(stats["total_reward"])  # Ensure type safety

    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Apply sigmoid activation function."""
        return 1 / (1 + np.exp(-x))

    def decide_move(self, state: np.ndarray) -> Tuple[bool, float]:
        """Decide whether to move up or down based on current state."""
        # Flatten the state matrix
        flat_state = state.flatten()

        # Forward pass through our network
        hidden = self._sigmoid(np.dot(flat_state, self.weights))
        # Average the node outputs for final decision
        probability = float(np.mean(hidden))

        # Simple threshold for movement
        return probability > 0.5, probability

    def learn(self, reward: float) -> None:
        """Update weights based on the reward received."""
        if self.last_state is None or self.last_probability is None:
            return

        # Flatten the last state
        flat_state = self.last_state.flatten()

        # Calculate the error gradient
        target = 1.0 if reward > 0 else 0.0
        error = target - self.last_probability

        # Update weights using gradient descent
        gradient = error * self.last_probability * (1 - self.last_probability)
        weight_updates = self.learning_rate * gradient * flat_state

        # Update all nodes
        for i in range(self.num_nodes):
            self.weights[:, i] += weight_updates

        # Track total reward
        self.total_reward += reward

    def update(self) -> None:
        """Update paddle position based on AI decision."""
        # Get current game state
        state = self.game_state.update(
            self.game_state.ball_x,
            self.game_state.ball_y,
            self.game_state.left_paddle_y,
            self.game_state.right_paddle_y,
        )

        # Decide and make move
        move_up, probability = self.decide_move(state)
        self.paddle.move(up=move_up)

        # Store state and action for learning
        self.last_state = state
        self.last_action = move_up
        self.last_probability = probability

        # Learn from immediate rewards
        if self.last_action is not None:
            # Only reward for hitting the ball
            if self.paddle.rect.colliderect(self.game_state.ball_rect):
                self.learn(0.1)  # Small reward for hitting

    def learn_from_human_games(self, games_file: str = "human_games.json") -> None:
        """Learn from recorded human gameplay."""
        try:
            with open(games_file, "r", encoding="utf-8") as f:
                points = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No recorded points found in {games_file}")
            return

        print(f"Learning from {len(points)} recorded points/rallies...")

        for point in points:
            # Only learn from points with good rallies
            if point["left_hits"] + point["right_hits"] < 2:
                continue

            # Learn from each frame
            for frame in point["frames"]:
                state = np.array(frame["state"])

                # Learn from left player if they hit the ball
                if frame["left_hit_ball"]:
                    if frame["left_moved_up"] is not None:  # They moved
                        self.last_state = state
                        self.last_action = frame["left_moved_up"]
                        # Target should be 1.0 for up, 0.0 for down
                        self.last_probability = 1.0 if frame["left_moved_up"] else 0.0
                        self.learn(0.1)  # Reward for hitting

                # Learn from right player if they hit the ball
                if frame["right_hit_ball"]:
                    if frame["right_moved_up"] is not None:  # They moved
                        self.last_state = state
                        self.last_action = frame["right_moved_up"]
                        # Target should be 1.0 for up, 0.0 for down
                        self.last_probability = 1.0 if frame["right_moved_up"] else 0.0
                        self.learn(0.1)  # Reward for hitting

        print("Finished learning from human games")

    def on_game_end(self, won: bool) -> None:
        """Called when a game ends."""
        self.games_played += 1

        # Big reward for winning with good play (10x normal win reward if 2+ hits)
        if won and self.last_state is not None:
            # Check if left or right paddle based on x position
            is_left_paddle = self.paddle.x < self.game_state.ball_x
            if is_left_paddle and self.game_state.left_hits >= 2:
                self.learn(10.0)  # Big reward for winning with 2+ hits
            elif not is_left_paddle and self.game_state.right_hits >= 2:
                self.learn(10.0)  # Big reward for winning with 2+ hits
            else:
                self.learn(1.0)  # Normal win reward
