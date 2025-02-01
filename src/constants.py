"""Constants used throughout the game."""

import pygame

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Drawing areas
SCORE_AREA_HEIGHT = 100  # Top area for scores
GAME_AREA_TOP = SCORE_AREA_HEIGHT
GAME_AREA_HEIGHT = WINDOW_HEIGHT - SCORE_AREA_HEIGHT - 50  # Bottom margin for info
INFO_AREA_HEIGHT = 50  # Bottom area for game info

# Game object dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = WHITE
PADDLE_COLOR = WHITE
SCORE_COLOR = WHITE
INFO_COLOR = WHITE

# Game settings
FPS = 60
PADDLE_SPEED = 5
BALL_SPEED = 5
SCORE_FONT_SIZE = 64
WINNER_FONT_SIZE = 48
INFO_FONT_SIZE = 32
RESET_DELAY_MS = 1000  # 1 second delay before ball reset
POINTS_TO_WIN = 5  # Points needed to win a game
GAMES_TO_WIN = 3  # Games needed to win the match

# Paddle positions (adjusted for game area)
LEFT_PADDLE_X = 50
RIGHT_PADDLE_X = WINDOW_WIDTH - 50 - PADDLE_WIDTH

# Control keys
# Player 1 (Left paddle)
P1_UP_KEY = pygame.K_w
P1_DOWN_KEY = pygame.K_s

# Player 2 (Right paddle)
P2_UP_KEY = pygame.K_UP
P2_DOWN_KEY = pygame.K_DOWN

# Score positions (in score area)
SCORE_MARGIN_TOP = 20  # Margin from top of score area
P1_SCORE_X = WINDOW_WIDTH // 4
P2_SCORE_X = 3 * WINDOW_WIDTH // 4

# Info positions
INFO_MARGIN_TOP = 10  # Margin from top of info area
GAMES_WON_Y = WINDOW_HEIGHT - INFO_AREA_HEIGHT // 2  # Centered in info area 