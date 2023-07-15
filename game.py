import pygame
from pygame.locals import *
from screen import Screen
from Gameboard.board import Board

from snake import Snake

pygame.init()

# Create the game window 
class Game:
    def __init__(self):
        self.is_running = False
        
        self.tiles = []
        # Add any other game-related variables here

    def init(self):
        pygame.init()
        self.screen = Screen(800, 600, "Snake", 5)
        self.all_sprites = pygame.sprite.Group()
        self.board = Board(self, 5)
        self.snake = Snake(self)
        self.running = True

    def run(self):
        self.init() 

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        self.cleanup()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            for tile in self.tiles: 
                tile.handle_event(event)

    def update(self):
        # Add game logic and update game objects here
        pass

    def draw(self):
        

        # Clear the screen
        self.screen.draw_grid()
        
        for tile in self.tiles:
            tile.draw()
        
        pygame.display.flip()

    def cleanup(self):
        print("Quitting")
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

pygame.quit()