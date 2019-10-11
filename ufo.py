import pygame
from pygame.sprite import Sprite
import random


class Ufo(Sprite):
    """A mysterious force class"""
    def __init__(self, ai_settings, screen):
        super(Ufo, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.image = pygame.image.load('images/ufo.png')
        self.rect = self.image.get_rect()
        self.active = False
        self.x = 3000
        self.speed = 1

    def blitme(self):
        """Draw the ufo at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x = (self.x + self.speed)
        self.rect.x = self.x

        """Move the Ufo right or left"""
        if self.x > 1200:
            self.speed = random.randint(1, 3)
            self.active = False
        if self.x > 10000:
            self.x = -10
        else:
            self.active = True
        # loop around
