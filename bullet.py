import pygame
from pygame.sprite import Sprite
import pygame.mask as mask


class Bullet(Sprite):
    """A class to mangae bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet obejct at the ship's current position. """
        super(Bullet, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/water_bullet2.png')

        # Create a bullet rect at (0,0) and then set correct position.
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Create bullet mask
        self.mask = mask.from_surface(self.image)

        # Store bullet's position as a decimal value
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the scene"""
        # Update the decimal position of the bullet
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y
        # update mask
        self.mask = pygame.mask.from_surface(self.image)

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.image, self.rect)
