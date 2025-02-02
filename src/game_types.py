"""Type definitions for game state.

This module contains dataclasses and type definitions used throughout the game.
"""

from dataclasses import dataclass
import pygame


@dataclass
class BallState:
    """Represents the state of the ball."""
    x: float = 0
    y: float = 0
    prev_x: float = 0
    rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    passed_paddle: bool = False
    hit_paddle: bool = False


@dataclass
class PaddleState:
    """Represents the state of both paddles."""
    left_y: float = 0
    right_y: float = 0
    left_hits: int = 0
    right_hits: int = 0 