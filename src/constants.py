"""Pong Game Constants.

This module defines all constants used in the Pong game, organized by their purpose:
- Window and Layout: Screen dimensions and area definitions
- Game Objects: Sizes and speeds of game elements
- UI Elements: Font sizes and positions
- Game Rules: Scoring and winning conditions
- Controls: Player input keys
"""

import pygame

# ====== Window and Layout ======
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Layout areas (divides screen into two sections)
HEADER_HEIGHT = 80  # Score display area
GAME_AREA_TOP = HEADER_HEIGHT
GAME_AREA_HEIGHT = WINDOW_HEIGHT - HEADER_HEIGHT
GAME_AREA_WIDTH = WINDOW_WIDTH  # Game area uses full window width

# ====== Game Objects ======
# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 4
PADDLE_MARGIN = 50  # Distance from screen edges

# Ball settings
BALL_SIZE = 15
BALL_SPEED = 5

# Paddle positions
LEFT_PADDLE_X = PADDLE_MARGIN
RIGHT_PADDLE_X = WINDOW_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH

# ====== UI Elements ======
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = WHITE
PADDLE_COLOR = WHITE
SCORE_COLOR = WHITE

# Font sizes
SCORE_FONT_SIZE = 48  # Current game score
WINNER_FONT_SIZE = 36  # Winner announcements

# Score positions in header
SCORE_MARGIN_TOP = 20
P1_SCORE_X = WINDOW_WIDTH // 3
P2_SCORE_X = (2 * WINDOW_WIDTH) // 3

# ====== Game Rules ======
FPS = 60  # Game speed
RESET_DELAY_MS = 1000  # Delay before ball reset after scoring
POINTS_TO_WIN = 5  # Points needed to win a game

# ====== Controls ======
# Player 1 (Left paddle)
P1_UP_KEY = pygame.K_w
P1_DOWN_KEY = pygame.K_s

# Player 2 (Right paddle)
P2_UP_KEY = pygame.K_UP
P2_DOWN_KEY = pygame.K_DOWN
