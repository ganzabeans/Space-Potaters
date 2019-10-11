import pygame
from pygame.sprite import Sprite


class Mini_Boom(Sprite):
    """Makes a mini explosion!!!"""
    def __init__(self, ai_settings, screen, rect):
        super(Mini_Boom, self).__init__()
        self.ai_settings = ai_settings
        self.images = ai_settings.mini_boom
        self.screen = screen
        self.active = True
        self.rect = rect
        self.anim_count = 0
    
    def blitme(self):
        """Draw the explosion at given location"""
        self.screen.blit(self.images[self.anim_count], self.rect)

    def mini_boom(self, ai_settings, timer):
        """ Checks time to see if change in anim frame is needed """
        if timer.ship_dict['switch']:
            self.change_image()
        self.blitme()

    def change_image(self):
        """Changes current frame for animation"""
        self.anim_count = (self.anim_count + 1) % 3
        self.blitme()
        if self.anim_count == 0:
            self.active = False
