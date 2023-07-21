import pygame

import assets.colours as colours


class Tile(pygame.sprite.Sprite):
    
    def __init__(self, interface, x, y, cell_size) -> None:
        super().__init__()
        self.interface = interface
        self.screen = interface.screen.surface
        self.width = self.height = cell_size
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colours.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x + 1
        self.rect.y = y + 1

        self.border = pygame.Surface([self.width + 10, self.height + 10])
        self.border.fill(colours.BLACK)
        self.border_rect = self.border.get_rect()
        self.border_rect.x = x 
        self.border_rect.y = y

        self.value = "_"
        self.hover = False
        self.colour = colours.GREEN

        self.interface.tiles.append(self)

    def __str__(self):
        return f" {self.value} "
    
    def draw(self):
        
        if type(self.value) == pygame.surface.Surface:
            self.screen.blit(self.value, (self.rect.x, self.rect.y))
        else:
            match self.value:
                case "B":
                    self.colour = colours.GREEN
                case "H":
                    self.colour = colours.GREEN_2        
                case "Dead":
                    self.colour = colours.CRIMSON
                case "A":
                    self.colour = colours.CRIMSON
                case "T":
                    self.colour = colours.CRIMSON
                case "_":
                    self.colour = colours.WHITE

            

            #pygame.draw.rect(self.screen, colours.BLACK, self.border_rect)
            pygame.draw.rect(self.screen, self.colour, self.rect)

