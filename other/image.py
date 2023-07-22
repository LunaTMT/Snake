import pygame

class Image:

    def __init__(self, interface) -> None:
        self.screen = interface.screen

    def set_to_cell_size(self, image):
        """
        This transforms the scale of provided pygame.image into the current screen cell size
        """
        return pygame.transform.scale(image, (self.screen.cell_size, self.screen.cell_size))

    
    def create(self, image_path):
        """
        Gets the image from the given path and loads it into pygame.image and returns a scaled to screen cell size image
        """
        image = pygame.image.load(image_path)
        return self.set_to_cell_size(image)