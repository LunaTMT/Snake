import pygame


import assets.colours as colours
from pygame.locals import *
from other.screen import Screen
from gameboard.board import Board
from sprites.snake import Snake
from sprites.apple import Apple
from gameboard.scoreboard import Scoreboard
from game.gamestate import GameState
from other.rectangle import Rectangle
from other.sound import Sound
from other.image import Image

# Create the game window 
class Game:

    

    def __init__(self, k):
        self.is_running = False
        self.start_time = None
        self.game_speed = None
        
        self.k = k
        self.tiles = []

        self.screen = Screen(self)
        self.sound = Sound()
        self.image = Image(self)
        

    def init(self):
        pygame.init()

        self.running = True
        self.clock = pygame.time.Clock()
        
        self.title_font = pygame.font.Font("assets/fonts/title.ttf", int(self.screen.width * 0.1))
        self.scoreboard_font = pygame.font.Font("assets/fonts/scoreboard.ttf", 2 * int(self.screen.cell_size))
        self.end_game_colour = colours.RED
        self.end_game_text = "You Lose"

        #init objects
        self.board      = Board(self)
        self.apple      = Apple(self)
        self.snake      = Snake(self)
        self.scoreboard = Scoreboard(self)

        


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
        #Upon final gamestate if the user presses any key the game is reinitialised
        if event.type == KEYDOWN:
            GameState.reset_states()
            self.init()


    def update(self):
        if GameState.play_game:
            self.snake.move() 

    def draw(self):
        self.board.draw()
        self.scoreboard.draw()

        if GameState.end_game:
            if self.is_timer_finished():
                self.draw_title(self.title_font, self.end_game_text, self.end_game_colour  , x=1 ,y=0.5)
                self.draw_title(self.title_font, "      Press any \n key to continue", colours.WHITE)
        
        pygame.display.flip()

    def cleanup(self):
        print("Quitting")
        pygame.quit()




    def draw_title(self, font, text, colour, x=1, y=1) -> None:
        """
        A simple method that will print on the screen a title of given parameters
        """
        title = font.render(text, True, colour)
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
    
    
    def start_timer(self):
        """
        Function to start the timer
        """
        self.start_time = pygame.time.get_ticks()

    
    def is_timer_finished(self):
        """
        This funciton checks if the timer has elapsed

        Before the function another time must be started elsewhere for the comparison in elapsed time,
        for example in:
        
        snake.py
        def check_bad_collisions(self, ...)
            ---
            ---
            self.interface.start_timer()
        """
        if self.start_time is None:
            return False

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        return elapsed_time >= 1000