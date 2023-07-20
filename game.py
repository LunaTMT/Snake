import pygame
import assets.colours as colours
from pygame.locals import *
from screen import Screen
from Gameboard.board import Board
from Sprites.snake import Snake
from Sprites.apple import Apple
from Gameboard.scoreboard import Scoreboard
from gamestate import GameState
from rectangle import Rectangle


# Create the game window 
class Game:
    def __init__(self, k):
        self.is_running = False
        self.k = k
        self.tiles = []        
        self.screen = Screen(self)

    def init(self):
        pygame.init()
         
        self.running = True
        self.clock = pygame.time.Clock()
        
        self.title_font = pygame.font.Font("assets/fonts/title.ttf", 65)
        self.scoreboard_font = pygame.font.Font("assets/fonts/scoreboard.ttf", 50)
        self.title_colour = colours.RED
        self.end_game_text = "You Lose"

        #init objects
        self.board      = Board(self)
        self.apple      = Apple(self)
        self.snake      = Snake(self)
        self.scoreboard = Scoreboard(self)

        self.start_time = None


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
            
            if GameState.play_game:
                self.snake.handle_event(event) 
            
            if GameState.end_game:
                self.check_any_key(event)
        
    def check_if_quit(self, event):
        if event.type == QUIT:
            self.running = False
    
    def check_any_key(self, event):
        if event.type == KEYDOWN:
            GameState.reset_states()
            self.init()


    def update(self):
        if GameState.play_game:
            self.snake.move() #This is the move method

    def draw(self):

    
        self.board.draw()
        self.scoreboard.draw()

        if GameState.end_game:
            if self.is_timer_finished():
                self.board.clear()
                self.draw_title(self.title_font, self.end_game_text, x=1 ,y=0.5)
                self.draw_title(self.title_font, "Please press any \n  key to continue")
        
        pygame.display.flip()

    def cleanup(self):
        print("Quitting")
        pygame.quit()

    def draw_title(self, font, text, x=1, y=1) -> None:
        """
        A simple method that will print on the screen a title of given parameters
        """
        title = font.render(text, True, self.title_colour)
        width, height = Rectangle.get_size(title)
        self.screen.surface.blit(title, self.get_centered_coord(width, height, x, y))

    def get_centered_coord(self, width, height, x_tranpose=1, y_transpose=1 ) -> int:
        """
        Gets the center coordinates based on an image or rect otherwise the image will be slightly off 
        when using self.center_x, self.center_y
        """
        center_x = (self.screen.width - width) // 2
        center_y = (self.screen.height - height) // 2
        return center_x * x_tranpose, center_y * y_transpose
    
    # Function to start the timer
    def start_timer(self):
        self.start_time = pygame.time.get_ticks()

    # Function to check if the timer has elapsed
    def is_timer_finished(self):
        
        if self.start_time is None:
            return False

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        return elapsed_time >= 1000