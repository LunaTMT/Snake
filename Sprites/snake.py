from pygame.locals import *
import assets.colours as colours
import random
from collections import deque
import pygame
import Gamestate

class Snake:
    
    def __init__(self, interface) -> None:
        self.interface      = interface
        self.board          = interface.board
        self.screen         = interface.screen
        self.apple          = interface.apple
        self.k              = interface.k


        self.positions = deque([])
        self.length = 3
        self.counter = 0
        self.value = "Snake"

        self.new_direction = self.direction = random.choice(("UP", "DOWN", "LEFT", "RIGHT"))
        
        self.set_move_time = 100  # Time in milliseconds for each move (half a second)
        self.last_move_time = 0
        self.last_draw_time = 0
        self.current_time = 0

        self._head = None
        self._tail = None

        self.opposite = {"UP"    : "DOWN",
                         "DOWN"  : "UP",
                         "LEFT"  : "RIGHT",
                         "RIGHT" : "LEFT"}

        self.direct_coord = {(-1, 0)  : "UP",
                             (1,  0)  : "DOWN",
                             (0, -1)  : "LEFT",
                             (0,  1)  : "RIGHT"}
        

        self.init_snake_positions()
   


    def init_snake_positions(self):
        #Init snake head position (our axis)
        head = r, c = self.board.generate_random_position(x_limit = 0.3, y_limit = 0.65)
        self.positions.append(head)

        #init Snake body
        match self.direction:
            case "UP":
                self.positions.appendleft((r+1, c))
                self.positions.appendleft((r+2, c))
            case "DOWN":
                self.positions.appendleft((r-1, c))
                self.positions.appendleft((r-2, c))
            case "LEFT":
                self.positions.appendleft((r, c+1))
                self.positions.appendleft((r, c+2))
            case "RIGHT":
                self.positions.appendleft((r, c-1))
                self.positions.appendleft((r, c-2))

        self.set_body("Snake")
            
        
    def handle_event(self, event):

            if event.type == KEYDOWN:
                
                if event.key == K_UP and self.direction != "UP":
                    self.new_direction = "UP"

                elif event.key == K_DOWN and self.direction != "DOWN":
                    self.new_direction = "DOWN"
                   
                elif event.key == K_LEFT and self.direction != "LEFT":
                    self.new_direction = "LEFT"
                
                elif event.key == K_RIGHT and self.direction != "RIGHT":
                    self.new_direction = "RIGHT"

    def set_body(self, value):
        #set the snek on the board
        for (r, c) in self.positions:
            self.board[r, c].value = value
    

    @property
    def head(self):
        self._head = self.positions[-1]
        return self._head
    
    @property
    def tail(self):
        self._tail = self.positions[0]
        return self._tail

    @tail.setter
    def tail(self, value):
        r, c = self.tail
        self.board[r, c].value = value
        self.positions.popleft()


    def move(self):
        self.current_time = pygame.time.get_ticks()
        if (self.current_time - self.last_move_time) >= self.set_move_time: #for every 0.5s  update
            
            self.check_winstate()

            if self.new_direction == self.opposite[self.direction]:
                self.new_direction = self.direction
            
            r, c = self.head
            match self.new_direction:
                case "UP":
                    new_position = (r-1, c)
                case "DOWN":
                    new_position = (r+1, c)
                case "LEFT":
                    new_position = (r, c-1)
                case "RIGHT":
                    new_position = (r, c+1)
                case _:
                    return
            
            if self.apple_collision():
                self.generate_new_tail()
                #self.board[self.apple.position].value = "O"
                self.apple.generate()
                self.length += 1
            
            elif self.check_collision(new_position):
                self.set_body("Dead")
                Gamestate.play_game = False
                Gamestate.end_game = True  
            else:
                #simply update head and remove tail to give appearance of movement
                self.positions.append(new_position)
                self.set_body(self.value)
                self.tail = "0"
                self.last_move_time = self.current_time
                self.direction = self.new_direction 

    def generate_new_tail(self):
        diff = tuple(map(lambda i, j: i - j, self.positions[-1], self.positions[-2]))    
        new_tail_position = tuple(map(lambda i, j: i + j, self.positions[-1], diff))  
        self.positions.append(new_tail_position)        

    def check_collision(self, position):
        r, c = position
        if (position in self.positions or self.board.check_out_of_bounds(position)):
            print(self.positions)
            return True
            
        return False
    
    def apple_collision(self):
        return True if self.positions[-1] == self.apple.position else False
    
    def check_winstate(self):
        
        if self.length == self.k**2:
            print(True)
            self.interface.end_game_text = "You Win!"
            self.interface.title_colour = colours.GREEN
            Gamestate.play_game = False
            Gamestate.end_game = True  
            