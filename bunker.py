import pygame
import pygame.surface
import pygame.mask as mask
from pygame.sprite import Sprite
import random
from PIL import Image
from PIL import ImageColor


class Bunker(Sprite):
    """This class manages the bunker and deletion of it."""

    def __init__(self, ai_settings, screen, letter):
        super(Bunker, self).__init__()
        self.screen = screen
        self.letter = letter
        self.ai_settings = ai_settings
        self.mydict = ai_settings.bunker_letters
        self.pygame_image = pygame.image.load(self.mydict[self.letter]
                                              ['image'][0])
        self.image = Image.open(self.mydict[self.letter]['image'][0])
        self.rect = self.pygame_image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.center = self.mydict[self.letter]['position']
        self.mask = mask.from_surface(self.pygame_image)

        # create a mask over image

    def blitme(self):
        """Draw the bunker at its current location"""
        # draw bunker
        self.screen.blit(self.pygame_image, self.rect)

    def destory_self(self, x, y, y_range, xmin, xmax, direction):
        # y_range = random.randint((y_range/2), y_range)
        for a in range(y_range):
            left, right = random.randint(int(xmin/2), xmin),\
                          random.randint(int(xmax/2), xmax)
            for x_val in range(x-left, x+right):
                self.mask.set_at((x_val, y + a*direction), 0)
                self.image.putpixel((x_val, y + a*direction), (0, 0, 0, 0))

        self.image.save(self.mydict[self.letter]['image'][1])
        self.pygame_image = pygame.image.load(self.mydict[self.letter]
                                              ['image'][1])
        self.blitme()
