import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.images = self.ai_settings.potato_skins

        # Load ship image and get its rect
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new shp at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a float for ship's center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

        # Animation markers
        self.anim_count = 0
        self.explosion = False
        self.invinsible = False

    def update(self):
        """Update the ship's position vased on the movement flag"""
        if not self.explosion:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor

        # update rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.images[self.anim_count], self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx
        
    """ Ship explosion animation """

    def ship_animate(self, ai_settings, timer):
        """ Checks time to see if change in anim frame is needed """
        if timer.ship_dict['switch']:
            self.change_image()
        else:
            self.blitme()

    def change_image(self):
        """Changes current frame for animation"""
        self.anim_count = (self.anim_count + 1) % 12
        if self.anim_count == 0:
            self.center_ship()
            self.invinsible = False
            self.explosion = False
        self.blitme()

    def set_explosion(self):
        """Ship hit, starts exploding"""
        self.explosion = True
        self.invinsible = True
