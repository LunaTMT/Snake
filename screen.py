import pygame
import assets.colours as colours

class Screen:
    
    def __init__(self, interface) -> None:
        self.k = interface.k
        self.width = self.height = self.init_dimensions()
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.colour = colours.WHITE
        pygame.display.set_caption("Snake")


    def init_dimensions(self):
        if self.k <= 10:
            self.cell_size = 50
      
        elif self.k <= 20:
            self.cell_size = 30

        elif self.k <= 40:
            self.cell_size = 20

        elif self.k <= 60:
            self.cell_size = 15

        return self.cell_size * (self.k)
        

