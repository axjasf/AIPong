"""Pong Game Player Classes.

This module contains the base Player class and its implementations:
- Base abstract Player class defining the interface
- HumanPlayer for keyboard-controlled players
- AIPlayer for computer-controlled players
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple
import numpy as np
import os
import json
from .paddle import Paddle
from .game_state import GameState
import random

class Player(ABC):
    """Abstract base class for all player types (human and AI)."""
    
    def __init__(self, paddle: Paddle):
        """Initialize the player with their paddle."""
        self.paddle = paddle
        self.score: int = 0
    
    @abstractmethod
    def update(self) -> None:
        """Update the player's paddle position based on their control method.
        
        This method must be implemented by concrete player classes to define
        how the paddle movement is controlled (keyboard, AI, etc).
        """
        pass
    
    def increment_score(self) -> None:
        """Increment the player's score by 1."""
        self.score += 1
    
    def reset_score(self) -> None:
        """Reset the player's score to 0."""
        self.score = 0

class HumanPlayer(Player):
    """Human-controlled player using keyboard input."""
    
    def __init__(self, paddle: Paddle, up_key: int, down_key: int):
        """Initialize the human player with their paddle and control keys."""
        super().__init__(paddle)
        self.up_key = up_key
        self.down_key = down_key
    
    def update(self) -> None:
        """Update paddle position based on keyboard input."""
        import pygame  # Import here to avoid circular import
        keys = pygame.key.get_pressed()
        
        if keys[self.up_key]:
            self.paddle.move(up=True)
        if keys[self.down_key]:
            self.paddle.move(up=False)

class AIPlayer(Player):
    """AI-controlled player using reinforcement learning."""
    
    def __init__(self, paddle: Paddle, game_state: GameState, num_nodes: int = 1, 
                 learning_rate: float = 0.02):
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
            self.weights = np.random.randn(total_inputs, num_nodes) * 0.1
        
        # Training data for learning
        self.last_state: Optional[np.ndarray] = None
        self.last_action: Optional[bool] = None
        self.last_probability: Optional[float] = None
        
        # Load or initialize training statistics
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
                self.games_played = stats['games_played']
                self.total_reward = stats['total_reward']
                self.last_save_milestone = (self.games_played // 100) * 100
        else:
            self.games_played: int = 0
            self.total_reward: float = 0
            self.last_save_milestone: int = 0
    
    def save_state(self) -> None:
        """Save weights and training stats to files."""
        # Save weights
        np.save(self.weights_file, self.weights)
        
        # Save stats
        stats = {
            'games_played': self.games_played,
            'total_reward': self.total_reward
        }
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f)
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Apply sigmoid activation function."""
        return 1 / (1 + np.exp(-x))
    
    def decide_move(self, state: np.ndarray) -> Tuple[bool, float]:
        """Decide whether to move up or down based on current state."""
        # Flatten the state matrix
        flat_state = state.flatten()
        
        # Forward pass through our simple network
        activations = self._sigmoid(np.dot(flat_state, self.weights))
        
        # For single node, use probability to decide
        probability = float(activations[0])
        return np.random.random() < probability, probability
    
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
        
        # Apply updates
        self.weights[:, 0] += weight_updates
        
        # Track total reward
        self.total_reward += reward
    
    def learn_from_human_games(self, games_file: str = "human_games.json"):
        """Learn from recorded human gameplay."""
        try:
            with open(games_file, 'r') as f:
                points = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No recorded points found in {games_file}")
            return
        
        print(f"Learning from {len(points)} recorded points/rallies...")
        
        for point in points:
            # Only learn from points with good rallies
            if point['left_hits'] + point['right_hits'] < 2:
                continue
            
            # Learn from each frame
            for frame in point['frames']:
                state = np.array(frame['state'])
                
                # Learn from left player if they hit the ball
                if frame['left_hit_ball']:
                    if frame['left_moved_up'] is not None:  # They moved
                        self.last_state = state
                        self.last_action = frame['left_moved_up']
                        self.last_probability = 0.8 if frame['left_moved_up'] else 0.2
                        self.learn(0.1)  # Reward for hitting
                
                # Learn from right player if they hit the ball
                if frame['right_hit_ball']:
                    if frame['right_moved_up'] is not None:  # They moved
                        self.last_state = state
                        self.last_action = frame['right_moved_up']
                        self.last_probability = 0.8 if frame['right_moved_up'] else 0.2
                        self.learn(0.1)  # Reward for hitting
            
            # Learn from the winner if they had good hits
            if point['winner'] == 'left' and point['winner_hits'] >= 2:
                self.learn(1.0)  # Big reward for winning with good play
            elif point['winner'] == 'right' and point['winner_hits'] >= 2:
                self.learn(1.0)  # Big reward for winning with good play
        
        # Save what we learned
        self.save_state()
        print("Finished learning from human games")
    
    def on_game_end(self, won: bool) -> None:
        """Called when a game ends."""
        self.games_played += 1
        
        # Big reward for winning with good play (10x normal win reward if 2+ hits)
        if won and self.last_state is not None:
            if self.paddle == self.game_state.left_paddle and self.game_state.left_hits >= 2:
                self.learn(10.0)  # Big reward for winning with 2+ hits
            elif self.paddle == self.game_state.right_paddle and self.game_state.right_hits >= 2:
                self.learn(10.0)  # Big reward for winning with 2+ hits
            else:
                self.learn(1.0)   # Normal win reward
        
        # Save state every 100 games (approximately 10% of 1000)
        current_milestone = (self.games_played // 100) * 100
        if current_milestone > self.last_save_milestone:
            self.save_state()
            self.last_save_milestone = current_milestone
    
    def update(self) -> None:
        """Update paddle position based on AI decision."""
        # Get current game state
        state = self.game_state.update(
            self.game_state.ball_x, self.game_state.ball_y,
            self.game_state.left_paddle_y, self.game_state.right_paddle_y
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
            # Only reward for hitting the ball, no penalties
            if self.paddle.rect.colliderect(self.game_state.ball_rect):
                self.learn(0.1)  # Reward for hitting 