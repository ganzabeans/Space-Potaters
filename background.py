import pygame


class Background():
    """ This class holds the background to the game!"""

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.image_list = ai_settings.bg_list
        self.b_type = 0
        self.image = pygame.image.load(self.image_list[
                                       self.b_type]).convert_alpha()
        self.rect = screen.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def switch_to(self, b_type):
        self.b_type = b_type
        self.image = pygame.image.load(self.image_list[
                                       self.b_type]).convert_alpha()
