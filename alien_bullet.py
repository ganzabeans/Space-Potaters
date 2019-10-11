import pygame
from pygame.sprite import Sprite
import pygame.mask as mask


class Abullet(Sprite):
    """A class to mangae bullets fired from the ship"""

    def __init__(self, ai_settings, screen, centerx, bottom):
        """Create a bullet obejct at the alien's current position. """
        super(Abullet, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/dna.png')

        # Create a bullet rect at (0,0) and then set correct position.
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom

        # Create mask for bunker collisions
        self.mask = mask.from_surface(self.image)

        # Store bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.a_bullet_color
        self.speed_factor = ai_settings.a_bullet_speed_factor

    def update(self):
        """Move the bullet up the scene"""
        # Update the decimal position of the bullet
        self.y += self.speed_factor
        # Update the rect position
        self.rect.y = self.y
        # Move mask to new position
        self.mask = pygame.mask.from_surface(self.image)

    def draw_a_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.image, self.rect)
