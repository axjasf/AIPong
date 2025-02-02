"""Game constants and configuration.

This module contains all the constant values used throughout the game:
- Window dimensions and layout
- Game object sizes and speeds
- Colors and visual settings
- Game rules and scoring
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
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
PADDLE_SPEED = 5
PADDLE_MARGIN = 50  # Distance from screen edges

# Ball settings
BALL_SIZE = 10
BALL_SPEED = 5
BALL_MAX_SPEED = 15
BALL_SPEED_INCREASE = 0.5

# Paddle positions
LEFT_PADDLE_X = PADDLE_MARGIN
RIGHT_PADDLE_X = WINDOW_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH

# ====== UI Elements ======
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BALL_COLOR = WHITE
PADDLE_COLOR = WHITE
SCORE_COLOR = WHITE
DIVIDER_COLOR = GRAY

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
POINTS_TO_WIN = 11  # Points needed to win a game
WIN_BY_TWO = True

# ====== Controls ======
# Player 1 (Left paddle)
P1_UP_KEY = pygame.K_w
P1_DOWN_KEY = pygame.K_s

# Player 2 (Right paddle)
P2_UP_KEY = pygame.K_UP
P2_DOWN_KEY = pygame.K_DOWN

# Display settings
FONT_SIZE = 36
SCORE_OFFSET = 20  # Distance from top of screen

# AI settings
REWARD_WIN = 1.0
REWARD_LOSE = -1.0
REWARD_HIT = 0.1
REWARD_MISS = -0.1

# Training settings
EXPLORATION_RATE = 0.1
LEARNING_RATE = 0.001
DISCOUNT_FACTOR = 0.99
BATCH_SIZE = 32
MEMORY_SIZE = 10000
UPDATE_TARGET_STEPS = 1000

# File paths
TRAINING_DATA_DIR = "training_data"
MODEL_SAVE_DIR = "models"
LOG_DIR = "logs"
