import pygame

import assets.colours as colours


class Tile(pygame.sprite.Sprite):
    
    def __init__(self, interface, x, y, cell_size) -> None:
        super().__init__()
        self.interface = interface
        self.screen = interface.screen.surface
        self.width = self.height = cell_size
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colours.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hover = False

        self.interface.tiles.append(self)

    def __str__(self):
        return f" ( x: {str(self.rect.x)}  y: {str(self.rect.y)}) "
    
    def draw(self):
        if self.hover:
            pygame.draw.rect(self.screen, colours.GREEN, self.rect)
        else:
            pygame.draw.rect(self.screen, colours.WHITE, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION: #update collide state
            if self.rect.collidepoint(event.pos):
                self.colour = colours.GOLD
                