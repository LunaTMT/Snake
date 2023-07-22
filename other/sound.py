import pygame

class Sound:
    def __init__(self) -> None:
        """
        Initialising all sounds effects in one class for Ez access
        """
        pygame.mixer.init()

        self.background = pygame.mixer.music.load("assets/sound/background.mp3")
        pygame.mixer.music.play(-1)
        
        self.chew = pygame.mixer.Sound("assets/sound/chew.wav")
        self.death = pygame.mixer.Sound("assets/sound/death.wav")
        self.hiss = pygame.mixer.Sound("assets/sound/hiss.wav")


