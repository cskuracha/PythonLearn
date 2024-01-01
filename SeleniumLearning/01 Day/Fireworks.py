import pygame
import sys
import random
import math
from pygame.locals import QUIT

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy New Year 2024 with Fireworks")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

# Set up font
font = pygame.font.Font(None, 36)

# Firework class
class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(COLORS)
        self.radius = 5
        self.vel_y = -random.uniform(8, 12)
        self.vel_x = random.uniform(-6, 6)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.2  # Gravity effect

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # Add sparkles
        for _ in range(5):
            sparkle_x = int(self.x + random.uniform(-10, 10))
            sparkle_y = int(self.y + random.uniform(-10, 10))
            pygame.draw.circle(screen, WHITE, (sparkle_x, sparkle_y), 1)

        # Add rocket lines
        pygame.draw.line(screen, WHITE, (int(self.x), int(self.y)), (int(self.x - self.vel_x), int(self.y - self.vel_y)))

# List to store fireworks
fireworks = []

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Create a new firework at random positions
    if random.random() < 0.03:
        fireworks.append(Firework(random.randint(0, WIDTH), HEIGHT))

    # Update and draw fireworks
    screen.fill(BLACK)

    for firework in fireworks:
        firework.move()
        firework.draw()

    fireworks = [fw for fw in fireworks if fw.y > 0]  # Remove fireworks that have gone off-screen

    # Display "Happy New Year 2024"
    text = font.render("Happy New Year 2024", True, random.choice(COLORS))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(30)
