import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien of a fleet"""

    def __init__(self, ai_settings, screen, alien_type, anim_start):
        """Initialize the alien and set starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.atype = alien_type
        self.time = pygame.time.get_ticks()
        self.anim_rate = ai_settings.alien_anim_rate
        self.anim_count = anim_start  # keeps track anim image

        # Load the alien image and set its rect attribute
        self.image_a = pygame.image.load(self.ai_settings.alien_type
                                         [self.atype]['image'][0])
        self.image_b = pygame.image.load(self.ai_settings.alien_type
                                         [self.atype]['image'][1])
        self.image = (self.image_a, self.image_b)
        self.rect = self.image[0].get_rect()

        # Start each new aliean near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image[self.anim_count], self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def alien_animate(self, ai_settings, timer):
        """ Checks time to see if change in anim frame is needed """
        if timer.alien_dict['switch']:
            self.change_image()
        else:
            self.blitme()

    def change_image(self):
        """Changes current frame for animation"""
        if self.anim_count == 1:
            self.anim_count = 0
        else:
            self.anim_count = 1

        self.blitme()

    def get_value(self):
        """returns point value of alien after being hit"""
        return self.ai_settings.alien_type[self.atype]['points']
