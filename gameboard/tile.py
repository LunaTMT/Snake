import pygame

import assets.colours as colours


class Tile(pygame.sprite.Sprite):
    
    GRASS = None

    def __init__(self, interface, x, y, cell_size) -> None:
        super().__init__()
        self.interface = interface
        self.screen = interface.screen.surface
        self.width = self.height = cell_size
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colours.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

        #Create the grass image once and store as class variable, unneccsary to do it for all K^2 tiles
        self.value =  interface.image.create("assets/images/grass.jpg") if not Tile.GRASS else Tile.GRASS
        Tile.GRASS = self.value

        self.interface.tiles.append(self)

    def draw(self):
        """
        Simply blits on the screen the current image value of the tile for its associated rectangle
        """
        self.screen.blit(self.value, (self.rect.x, self.rect.y))
