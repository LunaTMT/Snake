import pygame
import assets.colours as colours
from pygame.locals import *
from screen import Screen
from Gameboard.board import Board
from Sprites.snake import Snake
from Sprites.apple import Apple

import Gamestate
pygame.init()

# Create the game window 
class Game:
    def __init__(self, k):
        self.is_running = False
        self.k = k
        
        self.tiles = []        


        

    def init(self):
        pygame.init()
         
        self.running = True
        self.clock = pygame.time.Clock()
        
        self.title_font = pygame.font.Font("assets/fonts/title.ttf", 65)
        self.title_colour = colours.RED
        self.end_game_text = "You Loose"

        
        #init objects
        self.screen = Screen(self)
        self.board  = Board(self)
        self.apple  = Apple(self)
        self.snake  = Snake(self)
        
        self.all_sprites = pygame.sprite.Group()

        

    def run(self):
        self.init() 

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        self.cleanup()


    def handle_events(self):
        for event in pygame.event.get():
            self.check_if_quit(event)
            self.snake.handle_event(event) 
        

    def update(self):
        if Gamestate.play_game:
            self.snake.move() #This is the move method

    def draw(self):
        self.board.draw()

        if Gamestate.end_game:
            self.draw_title(self.title_font, self.end_game_text)


        pygame.display.flip()
        self.clock.tick(60)

    def cleanup(self):
        print("Quitting")
        pygame.quit()


    def check_if_quit(self, event):
        if event.type == QUIT:
            self.running = False


    def get_rect_size(self, rect) -> tuple[int]:
        """
        Gets the height and width of a rect object and returns it
        """
        rect = rect.get_rect()
        return  rect.width, rect.height

    def draw_title(self, font, text, x=1, y=1) -> None:
        """
        A simple method that will print on the screen a title of given parameters
        """
        title = font.render(text, True, self.title_colour)
        width, height = self.get_rect_size(title)
        self.screen.surface.blit(title, self.get_centered_coord(width, height, x, y))

    def get_centered_coord(self, width, height, x_tranpose=1, y_transpose=1 ) -> int:
        """
        Gets the center coordinates based on an image or rect otherwise the image will be slightly off 
        when using self.center_x, self.center_y
        """
        center_x = (self.screen.width - width) // 2
        center_y = (self.screen.height - height) // 2
        return center_x * x_tranpose, center_y * y_transpose