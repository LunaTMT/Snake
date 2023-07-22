import pygame

class Apple:

    def __init__(self, interface) -> None:
            self.interface  = interface
            self.board      = interface.board
            self.screen     = interface.screen
            self.k          = interface.k
            
            self.image      = interface.image.create("assets/images/apple.png")

            self.position = None
            self.value = None

            self.generate()

    def generate(self):
        """
        Gets a random position from the board and places the apple on the board
        """
        self.position = self.board.generate_random_position()
        self.board[self.position].value = self.image
    
    
