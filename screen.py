import pygame
import assets.colours as colours

class Screen:
    
    def __init__(self, width, height, caption, k=5) -> None:
        self.width = width 
        self.height = height
        self.surface = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.colour = colours.WHITE
        self.k = k
       
        self.init_grid_variables()
        pygame.display.set_caption(caption)
    
    def init_grid_variables(self):
        self.cell_width = self.width // self.k
        self.cell_height  = self.height // self.k
    
    def draw_grid(self):
        self.surface.fill (self.colour)

        # Draw horizontal lines
        for y in range(0, self.height, self.cell_height):
            pygame.draw.line(self.surface, (0, 0, 0), (0, y), (self.width, y))

        # Draw vertical lines
        for x in range(0, self.width, self.cell_width):
            pygame.draw.line(self.surface, (0, 0, 0), (x, 0), (x, self.height))
