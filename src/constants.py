"""Constants used throughout the game."""

import pygame

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Drawing areas
SCORE_AREA_HEIGHT = 80  # Reduced top area for scores
GAME_AREA_TOP = SCORE_AREA_HEIGHT
GAME_AREA_HEIGHT = WINDOW_HEIGHT - SCORE_AREA_HEIGHT - 60  # Adjusted game area
INFO_AREA_HEIGHT = 60  # Slightly increased bottom area

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
SCORE_FONT_SIZE = 48  # Reduced score size
WINNER_FONT_SIZE = 36
INFO_FONT_SIZE = 24  # Reduced info text size
RESET_DELAY_MS = 1000  # 1 second delay before ball reset
POINTS_TO_WIN = 5  # Points needed to win a game
GAMES_TO_WIN = 3  # Games needed to win the match

# Paddle positions (adjusted for game area)
PADDLE_MARGIN = 50  # Distance from edges
LEFT_PADDLE_X = PADDLE_MARGIN
RIGHT_PADDLE_X = WINDOW_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH

# Control keys
# Player 1 (Left paddle)
P1_UP_KEY = pygame.K_w
P1_DOWN_KEY = pygame.K_s

# Player 2 (Right paddle)
P2_UP_KEY = pygame.K_UP
P2_DOWN_KEY = pygame.K_DOWN

# Score positions (in score area)
SCORE_MARGIN_TOP = 20
P1_SCORE_X = WINDOW_WIDTH // 3  # Moved scores closer to center
P2_SCORE_X = (2 * WINDOW_WIDTH) // 3  # Moved scores closer to center

# Info positions
INFO_MARGIN_TOP = SCORE_AREA_HEIGHT + 10  # Adjusted for game area
GAMES_WON_Y = WINDOW_HEIGHT - (INFO_AREA_HEIGHT // 2)  # Centered in info area 