"""Player handling system.

This module contains the base Player class and its implementations:
- HumanPlayer: Handles human input
- ComputerPlayer: Simple rule-based computer player
- AIPlayer: Handles AI decision making
"""

from abc import ABC, abstractmethod
import json
import logging
import os
import random
from typing import Optional, Tuple, Literal

import numpy as np
import pygame
from numpy.typing import NDArray

from .constants import (
    BALL_SIZE,
    GAME_AREA_HEIGHT,
    GAME_AREA_TOP,
    GAME_AREA_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
)
from .game_state import GameState
from .paddle import Paddle
from .ball import Ball


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
        raise NotImplementedError

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


class ComputerPlayer(Player):
    """Computer player that follows the ball's vertical movement.

    This is a simple rule-based AI that attempts to track the ball's vertical position
    by moving the paddle up or down. It includes a small deadzone to prevent jitter
    and ensures the paddle stays within game boundaries.
    """

    # Deadzone in pixels to prevent paddle jitter
    MOVEMENT_DEADZONE = 10

    # Reaction delay ranges for different difficulties (in milliseconds)
    DELAY_RANGES = {
        "easy": (50, 200),    # Slower reactions
        "normal": (30, 50),   # Medium reactions
        "hard": (0, 30)       # Fast reactions
    }

    def __init__(self, paddle: Paddle, difficulty: Literal["easy", "normal", "hard"] = "normal") -> None:
        """Initialize the computer player.

        Args:
            paddle: The player's paddle
            difficulty: Difficulty setting affecting reaction time
        """
        super().__init__(paddle)
        self.ball: Optional[Ball] = None
        self.last_ball_y: float = 0.0
        
        # Set reaction delay based on difficulty
        min_delay, max_delay = self.DELAY_RANGES[difficulty]
        self.reaction_delay = random.randint(min_delay, max_delay)
        self.last_update_time = 0
        self.logger.info(
            "Computer player initialized with %dms reaction delay (%s mode)", 
            self.reaction_delay, 
            difficulty
        )

    def set_ball(self, ball: Ball) -> None:
        """Set the ball reference for the computer player.

        Args:
            ball: The game ball to track
        """
        self.ball = ball
        self.last_ball_y = ball.y

    def update(self) -> None:
        """Update paddle position based on ball's vertical movement.

        The paddle will move up or down to track the ball's vertical position,
        staying within the game area boundaries. A small deadzone prevents
        jitter when the ball is near the paddle's center.
        """
        if not self.ball:
            return

        # Check if enough time has passed since last update
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time < self.reaction_delay:
            return
        self.last_update_time = current_time

        # Calculate centers for comparison
        paddle_center = self.paddle.get_y() + (PADDLE_HEIGHT / 2)
        ball_center = self.ball.y + (BALL_SIZE / 2)

        # Only move if ball is outside the deadzone
        if abs(ball_center - paddle_center) > self.MOVEMENT_DEADZONE:
            # Calculate new position
            new_y = (
                self.paddle.get_y() - PADDLE_SPEED
                if ball_center < paddle_center
                else self.paddle.get_y() + PADDLE_SPEED
            )

            # Ensure paddle stays within game area
            new_y = max(GAME_AREA_TOP, min(new_y, GAME_AREA_TOP + GAME_AREA_HEIGHT - PADDLE_HEIGHT))

            self.paddle.set_y(new_y)

        # Track ball movement
        self.last_ball_y = self.ball.y


class AIPlayer(Player):
    """AI player that makes decisions based on game state."""

    def __init__(
        self,
        paddle: Paddle,
        game_state: GameState,
        num_nodes: int = 20,
        learning_rate: float = 0.02,
    ) -> None:
        """Initialize the AI player.

        Args:
            paddle: The player's paddle
            game_state: Current game state
            num_nodes: Number of hidden layer nodes
            learning_rate: Learning rate for weight updates
        """
        super().__init__(paddle)
        self.game_state = game_state
        self.num_nodes = num_nodes
        self.learning_rate = learning_rate

        # File paths for persistence
        self.weights_file = "ai_weights.npy"
        self.stats_file = "ai_stats.json"

        # Initialize or load weights
        state_size = game_state.get_state_size()
        if os.path.exists(self.weights_file):
            self.weights = np.load(self.weights_file)
        else:
            # Initialize weights for hidden layer with better scaling
            self.weights = np.random.randn(state_size, num_nodes) * np.sqrt(2.0 / state_size)

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
                self.games_played = int(stats["games_played"])
                self.total_reward = float(stats["total_reward"])

    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Apply sigmoid activation function.

        Args:
            x: Input array

        Returns:
            Array with sigmoid function applied
        """
        return 1 / (1 + np.exp(-x))

    def decide_move(self, state: np.ndarray) -> Tuple[bool, float]:
        """Decide whether to move up or down based on current state.

        Args:
            state: Current game state array

        Returns:
            Tuple of (move up decision, probability)
        """
        # Forward pass through our network
        hidden = self._sigmoid(np.dot(state, self.weights))
        # Average the node outputs for final decision
        probability = float(np.mean(hidden))

        # Simple threshold for movement
        return probability > 0.5, probability

    def learn(self, reward: float) -> None:
        """Update weights based on the reward received.

        Args:
            reward: Reward value for the last action
        """
        if self.last_state is None or self.last_probability is None:
            return

        # Calculate the error gradient
        target = 1.0 if reward > 0 else 0.0
        error = target - self.last_probability

        # Update weights using gradient descent
        gradient = error * self.last_probability * (1 - self.last_probability)
        weight_updates = self.learning_rate * gradient * self.last_state

        # Update all nodes
        for i in range(self.num_nodes):
            self.weights[:, i] += weight_updates

        # Track total reward
        self.total_reward += reward

    def update(self) -> None:
        """Update paddle position based on AI decision."""
        # Get current game state
        state = self.game_state.get_state()

        # Decide and make move
        move_up, probability = self.decide_move(state)
        new_y = (
            self.paddle.get_y() - PADDLE_SPEED if move_up else self.paddle.get_y() + PADDLE_SPEED
        )

        # Ensure paddle stays within game area
        if GAME_AREA_TOP <= new_y <= GAME_AREA_TOP + GAME_AREA_HEIGHT - PADDLE_HEIGHT:
            self.paddle.set_y(new_y)

        # Store state and action for learning
        self.last_state = state
        self.last_action = move_up
        self.last_probability = probability

        # Learn from immediate rewards
        if self.last_action is not None:
            # Only reward for hitting the ball
            ball_rect = pygame.Rect(
                state[0] * (GAME_AREA_WIDTH / 2) + GAME_AREA_WIDTH / 2,
                state[1] * (GAME_AREA_HEIGHT / 2) + GAME_AREA_TOP + GAME_AREA_HEIGHT / 2,
                BALL_SIZE,
                BALL_SIZE,
            )
            if self.paddle.rect.colliderect(ball_rect):
                self.learn(0.1)  # Small reward for hitting

    def learn_from_human_games(self, games_file: str = "human_games.json") -> None:
        """Learn from recorded human gameplay.

        Args:
            games_file: Path to the recorded games file
        """
        try:
            with open(games_file, "r", encoding="utf-8") as f:
                points = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning("No recorded points found in %s", games_file)
            return

        self.logger.info("Learning from %d recorded points/rallies", len(points))

        for point in points:
            # Only learn from points with good rallies
            hits = point.get("left_hits", 0) + point.get("right_hits", 0)
            if hits < 2:
                continue

            # Learn from each frame
            for frame in point.get("frames", []):
                state = np.array(frame.get("state", []))
                if len(state) != self.game_state.get_state_size():
                    continue

                # Learn from left player if they hit the ball
                if frame.get("left_hit_ball"):
                    if frame.get("left_moved_up") is not None:  # They moved
                        self.last_state = state
                        self.last_action = frame["left_moved_up"]
                        self.last_probability = 1.0 if frame["left_moved_up"] else 0.0
                        self.learn(0.1)  # Reward for hitting

                # Learn from right player if they hit the ball
                if frame.get("right_hit_ball"):
                    if frame.get("right_moved_up") is not None:  # They moved
                        self.last_state = state
                        self.last_action = frame["right_moved_up"]
                        self.last_probability = 1.0 if frame["right_moved_up"] else 0.0
                        self.learn(0.1)  # Reward for hitting

        self.logger.info("Finished learning from human games")

    def on_game_end(self, won: bool) -> None:
        """Called when a game ends.

        Args:
            won: Whether this player won the game
        """
        self.games_played += 1

        # Big reward for winning with good play (10x normal win reward if 2+ hits)
        if won and self.last_state is not None:
            # Check if left or right paddle based on x position
            is_left_paddle = self.paddle.x < self.game_state.get_state()[0]
            hits = 0  # We'll calculate hits from the state
            if is_left_paddle:
                hits = sum(1 for s in self.game_state.get_state() if s[0] < 0)
            else:
                hits = sum(1 for s in self.game_state.get_state() if s[0] > 0)

            if hits >= 2:
                self.learn(10.0)  # Big reward for winning with 2+ hits
            else:
                self.learn(1.0)  # Normal win reward

    def save_model(self, filename: str) -> None:
        """Save the AI model weights and stats.

        Args:
            filename: Base filename to save to
        """
        # Save weights
        weights_file = f"{filename}_weights.npy"
        np.save(weights_file, self.weights)

        # Save stats
        stats_file = f"{filename}_stats.json"
        stats = {
            "games_played": self.games_played,
            "total_reward": self.total_reward,
        }
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f)

        self.logger.info("Saved model to %s", filename)
