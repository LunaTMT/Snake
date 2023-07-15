import pygame
from pygame.locals import *

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Rectangle class
class Rectangle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        # Draw a border rectangle with a black color
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 1)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rectangle with Border in Pygame")

# Create a sprite group
all_sprites = pygame.sprite.Group()

# Add rectangles to the group
tile1 = Rectangle(100, 200, 50, 50, GREEN)
tile2 = Rectangle(300, 150, 80, 40, GREEN)
all_sprites.add(tile1, tile2)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw all sprites in the group
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
