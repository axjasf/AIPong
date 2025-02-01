"""Pong Game Player Classes.

This module contains the base Player class and its implementations:
- Base abstract Player class defining the interface
- HumanPlayer for keyboard-controlled players
- (Future) AIPlayer for computer-controlled players
"""

from abc import ABC, abstractmethod
from typing import Optional
from .paddle import Paddle

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