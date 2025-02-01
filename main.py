import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 45  # Starting angle in degrees
        self.velocity = 5
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
    
    def move(self, paddles):
        # Convert angle to radians for math functions
        rad_angle = math.radians(self.angle)
        
        # Calculate new position
        new_x = self.x + (self.velocity * math.cos(rad_angle))
        new_y = self.y + (self.velocity * math.sin(rad_angle))
        
        # Update rect for collision detection
        self.rect.x = int(new_x)
        self.rect.y = int(new_y)
        
        # Wall collisions (top and bottom)
        if new_y <= 0 or new_y >= WINDOW_HEIGHT - BALL_SIZE:
            self.angle = -self.angle  # Reflect angle
        
        # Paddle collisions
        for paddle in paddles:
            if self.rect.colliderect(paddle.rect):
                self.angle = 180 - self.angle
                break
        
        # Update position
        self.x = new_x
        self.y = new_y

class Paddle:
    def __init__(self, x):
        self.x = x
        self.y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.speed = 5
        self.rect = pygame.Rect(x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    def move(self, up=False):
        if up and self.y > 0:
            self.y -= self.speed
        elif not up and self.y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            self.y += self.speed
        self.rect.y = self.y

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Simple Pong")
    clock = pygame.time.Clock()
    
    # Create game objects
    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    left_paddle = Paddle(50)
    right_paddle = Paddle(WINDOW_WIDTH - 50 - PADDLE_WIDTH)
    paddles = [left_paddle, right_paddle]
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Handle continuous keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(up=True)
        if keys[pygame.K_s]:
            left_paddle.move(up=False)
        if keys[pygame.K_UP]:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN]:
            right_paddle.move(up=False)
        
        # Update game state
        ball.move(paddles)
        
        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle.rect)
        pygame.draw.rect(screen, WHITE, right_paddle.rect)
        pygame.draw.rect(screen, WHITE, ball.rect)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()