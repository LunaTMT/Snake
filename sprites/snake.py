import pygame
import random

from pygame.locals import *
from collections import deque

import assets.colours as colours

from game.gamestate import GameState
from gameboard.tile import Tile

class Snake:
    
    def __init__(self, interface=None) -> None:
        self.interface      = interface

        #interface objects
        self.board          = interface.board
        self.screen         = interface.screen
        self.apple          = interface.apple
        self.sound          = interface.sound
        self.image          = interface.image

        #interface variables
        self.k              = interface.k
        
        #interface text-related atributes
        self.draw_title     = interface.draw_title
        self.title_font     = interface.title_font
        self.end_game_text  = interface.end_game_text

        
        #The snake begins in a random direction
        self.new_direction = self.direction = random.choice(("UP", "DOWN", "LEFT", "RIGHT"))
        
        #Used for each tick of snake movement 
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
        
        #This counter is used for random head image selection such that it doesn't look strange to the eye
        self.counter = 0

        self.init_images() 

        self.body = Body(self, self.board) #the body is a deque 
        self.init_snake_positions() #init the beginning snake on the board
        




    def init_snake_positions(self) -> None:
        """
        for the initialisation of our snake we get a random position on the board
        The random position is limited to a sqaure in the center with dimensions:
            - 30% screen.width 
            - 65% screen height 

        The limit on the position is such that the snake doesnt spawn in a zone that will instantly kill it
        There's no fun in that right?
        """
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

              
    def init_images(self) -> None:
        """
        Initialising all images to be used with the snake sprite
        """
        self.head_image = self.image.create("assets/images/snake_head.png")
        self.head_tongue_image = self.image.create("assets/images/snake_head_tongue.png")
        self.head_mouth_open_image = self.image.create("assets/images/snake_head_mouth_open.png")
        self.head_eyes_closed_image = self.image.create("assets/images/snake_head_eyes_closed.png")
        self.snake_head_dead = self.image.create("assets/images/snake_head_dead.png")

        self.body_image = self.image.create("assets/images/snake_body.png")
        self.tail_image = self.image.create("assets/images/snake_tail.png")
        


    def handle_event(self, event):
        """
        When the user press a key the direction of the snake is changed

        The new direction only changes when the inputed direction is unique 
        and does not give way to contradiction
        """
        if event.type == KEYDOWN:
            
            if event.key == K_UP and self.direction != "UP":
                self.new_direction = "UP"

            elif event.key == K_DOWN and self.direction != "DOWN":
                self.new_direction = "DOWN"
            
            elif event.key == K_LEFT and self.direction != "LEFT":
                self.new_direction = "LEFT"
            
            elif event.key == K_RIGHT and self.direction != "RIGHT":
                self.new_direction = "RIGHT"

            """The following conditional ensures a contradiction doesn't exist before the next tick is set
            As the user can change the position multiple times between a tick 
            there can arise occurences where the next direction becomes its opposite

            E.g.

            current_direction = up
            game tick - 1
            
            event K_RIGHT           (VALID)
            new_direction = RIGHT
            
            event K_DOWN            (ALSO VALID BECAUSE IT DOESNT CONTRADICT THE NEW DIRECTION)
            new_direction = DOWN
            
            game tick end

            In this case the new direction is invalid as it is the current_directions opposite
            We can have the snake going back in upon itself it would immediately die,
            We must ignore such directions by setting it to its previous

            In the above case:
            new_direction becomes up 
            i.e. the current direction does not change
            
            """
            if self.new_direction == self.opposite_direction[self.direction]:
                self.new_direction = self.direction
            
    def get_new_position(self, start, direction):
        """
        Given a position and a direction
        a new position is return based upon the direction of movement
        """
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
        """
        This function is where the magic happens:
        
        - for each game tick (screen.game_speed)

            - The snake length is checked to see if the user has won (len snake == k^2)
            - The new position is generated
            - There is a collision check between the new position and:
                    - The snake or the board (check_bad_collisions) or with
                    - The apple
            - the body is then updated with the new position
            - and the head with its appropriate image
                - dead or 
                - eating
            (Respectively)
        """
        self.current_time = pygame.time.get_ticks()
        if (self.current_time - self.last_move_time) >= self.set_move_time: #for every 0.5s  update
            self.last_move_time = self.current_time


            if self.check_winstate():
                return 
            
            new_position = self.get_new_position(self.body.head, self.new_direction)
            head = None

            if self.check_bad_collisions(new_position):
                self.body.head = self.snake_head_dead               
                self.sound.death.play()

            else:
                if self.check_apple_collision(new_position):
                    head = self.head_mouth_open_image
                    self.body.generate_tail()
                    self.apple.generate()
                    self.sound.chew.play()
                    
                self.body.append(new_position)
                self.body.update(head)

                head = None
                self.direction = self.new_direction


                                
                
                

    def get_direction(self, position_1 , position_2):
        """
        Given any two positions this function finds the direction in which the first position is going
        e.g.
        
        (0,0) , (0, 1) is going RIGHT 
        The head is (0,1) (is always [-1])
        """
        return self.coordinate_direction[self.get_coord_difference(position_1, position_2)]

    def get_coord_difference(self, position_1, position_2):
        """
        This function returns the difference between two tuples - (r,c)
        """
        return tuple(map(lambda i, j: i - j, position_1, position_2))    
    
    def get_rotated_image(self, image, direction):
        """
        This function rotates an image based upon its direction
        It is used only for the head and tail such that is will always be facing the correct direction
        """
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
        """
        This function attempts to choose a head for the snake so it looks realistic 
        and not just a random choice between multiple heads
        The attempt is to at least give the apperance of a real snake 
        """
        self.counter += 1

        #Every 20 ticks so the snake doesnt look like it is having a seziure
        if 20 <= self.counter <= 23:
            return self.head_eyes_closed_image
        
        #Ever 10 ticks we make a hiss sound and show the head with its tongue out 
        elif not (self.counter % 10):
            self.sound.hiss.play()
            return self.head_tongue_image
        
        elif self.counter > 23:
            self.counter = 0
        #Returning the default head if our tick counter is > 23
        return self.head_image
            
                    
    def check_bad_collisions(self, position):
        """
        This function checks to see if the new position is either 
        already a snake position (self collision) OR a position outside the board (board collision)

        Gamestate is changed accordingly it the collision is True
        """
        r, c = position
        if (position in self.body or self.board.check_out_of_bounds(position)):

            #Gamestate change
            GameState.play_game = False
            GameState.end_game = True  
            self.interface.start_timer()

            return True
        return False
    
    def check_apple_collision(self, position):
        """
        If the given position has the same position as the apple then a collision exists (True)
        """
        return True if position == self.apple.position else False

    def check_winstate(self):
        """
        If the snake length is the area of the board (K^2),
        then the user has won

        Gamestate is changed accordingly following this
        """
        if self.body.length == self.k**2:
            self.interface.end_game_text = "You Win!"
            self.interface.end_game_colour = colours.GREEN

            GameState.play_game = False
            GameState.end_game = True  
            self.interface.start_timer()

            return True 
        return False

class Body(deque):
    """
    This class was created in order that appending to the body 
    would make the move funciton above clearer and cleaner.
    """
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
        """Easy access to head of snake using attribute body.head for cleaner notation instead of body[-1]"""
        self._head = self[-1]
        return self._head
    
    @head.setter
    def head(self, value):
        """
        Setting the tail with the given value
        """
        
        #Rotating the image given its direction
        if type(value) == pygame.surface.Surface:
            direction = self.get_direction(self.head, self[-2])
            value = self.get_rotated_image(value, direction)

        self.board[self.head].value = value

    @property
    def tail(self):
        """
        Easy access to tail of snake using attribute body.tail for cleaner notation instead of body[0]
        """
        self._tail = self[0]
        return self._tail

    @tail.setter
    def tail(self, value):
        """
        Setting the tail with the given value
        """

        try:
            #To give the appearance of movement we must remove the old tail and set it to its default tile (GRASS)
            self.board[self.tail].value = Tile.GRASS
        except:
            #In instances where the snake eats an apple the tail may be shifted to an invalid position
            #Either way we still remove it from the deque in the next line
            pass
        
        self.popleft()

        #Rotating the image given its direction
        if type(value) == pygame.surface.Surface:
            direction = self.get_direction(self.tail, self[1])
            value = self.get_rotated_image(value, direction)

        
        self.board[self.tail].value = value


    def set_body(self):
        """
        This function sets all positions except head and tail of the deque to the body image
        """
        for i in range(1, len(self)-1):
            self.board[self[i]].value = self.body_image
        
   


    def update(self, head=None):
        #set the snek on the board
        self.set_body()
        self.tail = self.tail_image
        self.head = head if head else self.get_random_head_image()

        """
        The passed head value could be a head based upon gamestate:
        E.g
            - Dead
            - Eating
        """

        
    def generate_tail(self):
        """
        This function generate a new tail position depending up the current tail direction
        """
        new_r, new_c = self.get_coord_difference(self.tail, self[1]) 
        r, c = self.tail
        self.appendleft((r + new_r, c + new_c))
        self.length += 1
