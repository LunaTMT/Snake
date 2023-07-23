import pygame
import assets.colours as colours

class Screen:
    
    def __init__(self, interface) -> None:
        self.interface  = interface
        self.k          = interface.k

        self.width = self.height = self.init_dimensions()

        self.surface = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.colour = colours.WHITE
        pygame.display.set_caption("Snake")

    

    def init_dimensions(self):
        """
        Based upon the size of the board which is passed as an argument in main.py (k)
        The screen size and the game speed is altered accordingly for a relatively comfortable playing experience
        """
        if self.k <= 5:
            self.cell_size = 50
            self.interface.game_speed = 500
        
        elif self.k <= 10:
            self.cell_size = 40
            self.interface.game_speed = 200
      
        elif self.k <= 20:
            self.cell_size = 30
            self.interface.game_speed = 100
            
        elif self.k <= 40:
            self.cell_size = 25
            self.interface.game_speed = 100

        else:
            self.cell_size = 20
            self.interface.game_speed = 50

        return self.cell_size * (self.k)
        

