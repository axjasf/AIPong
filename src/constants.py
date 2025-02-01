"""Constants used throughout the game."""

import pygame

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Game object dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = WHITE  # Ball color, can be changed independently if needed
PADDLE_COLOR = WHITE  # Paddle color, can be changed independently if needed

# Game settings
FPS = 60
PADDLE_SPEED = 5
BALL_SPEED = 5
SCORE_FONT_SIZE = 64
WINNER_FONT_SIZE = 48
RESET_DELAY_MS = 1000  # 1 second delay before ball reset
WINNING_SCORE = 5  # Score needed to win the game

# Paddle positions
LEFT_PADDLE_X = 50
RIGHT_PADDLE_X = WINDOW_WIDTH - 50 - PADDLE_WIDTH

# Control keys
# Player 1 (Left paddle)
P1_UP_KEY = pygame.K_w
P1_DOWN_KEY = pygame.K_s

# Player 2 (Right paddle)
P2_UP_KEY = pygame.K_UP
P2_DOWN_KEY = pygame.K_DOWN

# Score positions
SCORE_MARGIN_TOP = 50
P1_SCORE_X = WINDOW_WIDTH // 4
P2_SCORE_X = 3 * WINDOW_WIDTH // 4 