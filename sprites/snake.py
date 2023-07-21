from pygame.locals import *
import assets.colours as colours
import random
from collections import deque
import pygame
from game.gamestate import GameState

class Snake:
    
    def __init__(self, interface=None) -> None:
        self.interface      = interface
        self.board          = interface.board
        self.screen         = interface.screen
        self.apple          = interface.apple
        self.k              = interface.k

        self.draw_title     = interface.draw_title
        self.title_font     = interface.title_font
        self.end_game_text  = interface.end_game_text

        

        self.new_direction = self.direction = random.choice(("UP", "DOWN", "LEFT", "RIGHT"))
        
        self.set_move_time = interface.game_speed  # Time in milliseconds for each move (half a second)
        self.last_move_time = 0
        self.current_time = 0

        self.opposite_direction = {
                        "UP"    : "DOWN",
                        "DOWN"  : "UP",
                        "LEFT"  : "RIGHT",
                        "RIGHT" : "LEFT"}

        self.coordinate_direction = {
                        (-1,  0)  : "UP",
                        (1,   0)  : "DOWN",
                        (0,  -1)  : "LEFT",
                        (0,   1) : "RIGHT"}
    
        self.counter = 0

        self.init_images()
        self.body = Body(self, self.board)
        self.init_snake_positions()
        




    def init_snake_positions(self):
        #Init snake head position (our axis)
        head = r, c = self.board.generate_random_position(x_limit = 0.3, y_limit = 0.65)
        self.body.append(head)

        #init Snake body
        match self.direction:
            case "UP":
                self.body.appendleft((r+1, c))
                self.body.appendleft((r+2, c))
            case "DOWN":
                self.body.appendleft((r-1, c))
                self.body.appendleft((r-2, c))
            case "LEFT":
                self.body.appendleft((r, c+1))
                self.body.appendleft((r, c+2))
            case "RIGHT":
                self.body.appendleft((r, c-1))
                self.body.appendleft((r, c-2))

              
    def init_images(self):
        
        def set_to_cell_size(image):
            return pygame.transform.scale(image, (self.screen.cell_size, self.screen.cell_size))

        self.head_image = pygame.image.load("assets/images/snake_head.png")
        self.head_image = set_to_cell_size(self.head_image)

        self.dead_head_image = pygame.image.load("assets/images/dead_snake_head.png")
        self.dead_head_image = set_to_cell_size(self.dead_head_image)

        self.head_tongue_image = pygame.image.load("assets/images/snake_head_tongue.png")
        self.head_tongue_image = set_to_cell_size(self.head_tongue_image)

        self.head_eyes_closed_image = pygame.image.load("assets/images/snake_head_eyes_closed.png")
        self.head_eyes_closed_image = set_to_cell_size(self.head_eyes_closed_image)  

        self.body_image = pygame.image.load("assets/images/snake_body.png")
        self.body_image = set_to_cell_size(self.body_image)

        self.tail_image = pygame.image.load("assets/images/snake_tail.png")
        self.tail_image = set_to_cell_size(self.tail_image)


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

                if self.new_direction == self.opposite_direction[self.direction]:
                    self.new_direction = self.direction
            
    def get_new_position(self, start, direction):
        r, c = start
        match direction:
            case "UP":
                return (r-1, c)
            case "DOWN":
                return (r+1, c)
            case "LEFT":
                return (r, c-1)
            case "RIGHT":
                return (r, c+1)
            case _:
                return


    def move(self):
        self.current_time = pygame.time.get_ticks()
        if (self.current_time - self.last_move_time) >= self.set_move_time: #for every 0.5s  update
            self.last_move_time = self.current_time


            self.check_winstate()
            
            new_position = self.get_new_position(self.body.head, self.new_direction)

                
            if self.check_bad_collisions(new_position):
                self.body.head = self.dead_head_image
                
            else:
                if self.check_apple_collision(new_position):
                    #set head to open mouth
                    self.body.eat()
                    self.apple.generate()

                self.body.append(new_position)
                self.body.update()
                self.direction = self.new_direction

            #self.board.print_board()

                                
                
                

    def get_direction(self, position_1 , position_2):
        return self.coordinate_direction[self.get_coord_difference(position_1, position_2)]

    def get_coord_difference(self, position_1, position_2):
        "this function returns what the directional difference is between two points"
        return tuple(map(lambda i, j: i - j, position_1, position_2))    
    
    def get_rotated_image(self, image, direction):
        match direction:
            case "UP":
                angle = 0
            case "DOWN":
                angle = 180
            case "LEFT":
                angle = 90
            case "RIGHT":
                angle = 270

        return pygame.transform.rotate(image, angle)

    def get_random_head_image(self):
        
        self.counter += 1
        if 20 <= self.counter <= 23:
            return self.head_eyes_closed_image
        
        elif not (self.counter % 5):
            return self.head_tongue_image
        
        elif self.counter > 23:
            self.counter = 0
        
        return self.head_image
            
                    
        


    def check_bad_collisions(self, position):
        r, c = position
        if (position in self.body or self.board.check_out_of_bounds(position)):

            #Gamestate change
            GameState.play_game = False
            GameState.end_game = True  
            self.interface.start_timer()

            return True
            
        return False
    
    def check_apple_collision(self, position):
        return True if position == self.apple.position else False

    def check_winstate(self):
        
        if self.body.length == self.k**2:
            self.interface.end_game_text = "You Win!"
            self.interface.title_colour = colours.GREEN
            
            GameState.play_game = False
            GameState.end_game = True  
            

class Body(deque):

    def __init__(self, snake, board) -> None:
        self.snake                  = snake
        self.get_direction          = snake.get_direction
        self.get_rotated_image      = snake.get_rotated_image
        self.get_random_head_image  = snake.get_random_head_image
        self.get_coord_difference   = snake.get_coord_difference
        
        self.body_image         = snake.body_image
        self.tail_image         = snake.tail_image
        self.board = board

        self.length = 3
        self._head = None
        self._tail = None


    @property
    def head(self):
        self._head = self[-1]
        return self._head
    
    @head.setter
    def head(self, value):
        self.set_body()      

        if type(value) == pygame.surface.Surface:
            direction = self.get_direction(self.head, self[-2])
            value = self.get_rotated_image(value, direction)

        self.board[self.head].value = value

    @property
    def tail(self):

        self._tail = self[0]
        return self._tail

    @tail.setter
    def tail(self, value):
        try:
            self.board[self.tail].value = "_"
        except:
            pass
        
        self.popleft()

        
        if type(value) == pygame.surface.Surface:
            direction = self.get_direction(self.tail, self[1])
            value = self.get_rotated_image(value, direction)

        
        self.board[self.tail].value = value




        
    def set_body(self):

        for i in range(1, len(self)-1):
            position_1 = self[i]
            position_2 = self[i+1]
            direction = self.get_direction(position_2, position_1)
            value = self.get_rotated_image(self.body_image, direction)

            self.board[position_1].value = self.body_image
        
   


    def update(self):
        #set the snek on the board
        self.set_body()
        self.tail = self.tail_image
        self.head = self.get_random_head_image()

          

    def eat(self):
        new_r, new_c = self.get_coord_difference(self.tail, self[1]) 
        r, c = self.tail
        self.appendleft((r + new_r, c + new_c))
        self.length = len(self)
