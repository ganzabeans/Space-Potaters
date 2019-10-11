import pygame
from pygame import time


class Settings():
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's statiec settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.frames = [1, 2, 3, 4, 5]
        self.bg_rect = (0, 0)
        self.bg_list = ('images/start.png', 'images/background.png')

        # Ship settings
        self.ship_limit = 3

        # Bunker settings
        self.bunker_screen_height = 650
        self.potato = ('p', 'o', 't', 'a', 'T', 'O')
        self.bunker_letters = {
                               'p': {'image': ('images/p.png',
                                               'images/p_temp.png'),
                                     'position': (100,
                                                  self.bunker_screen_height)},
                               'o': {'image': ('images/o.png',
                                               'images/o_temp.png'),
                                     'position': (300,
                                                  self.bunker_screen_height)},
                               't': {'image': ('images/t.png',
                                               'images/t_temp.png'),
                                     'position': (500,
                                                  self.bunker_screen_height)},
                               'a': {'image': ('images/a.png',
                                               'images/a_temp.png'),
                                     'position': (700,
                                                  self.bunker_screen_height)},
                               'T': {'image': ('images/t2.png',
                                               'images/t2_temp.png'),
                                     'position': (900,
                                                  self.bunker_screen_height)},
                               'O': {'image': ('images/o2.png',
                                               'images/o2_temp.png'),
                                     'position': (1100,
                                                  self.bunker_screen_height)},
                               }
        self.bunker_max = 15
        self.bunker_left = -1
        self.bunker_right = 1
        self.bunker_bullet_offset = -5

        # Button settings
        self.buttons = {
                        'play': {'message': 'Play!!!',
                                 'position': (600, 400)},
                        'hs': {'message': "High Scores",
                               'position': (600, 500)},
                        'back': {'message': "Back",
                                 'position': (600, 750)}
                        }
        self.button_width = 350
        self.button_height = 80
        self.button_color = (9, 255, 182)
        self.button_text_color = (0, 0, 0)

        # Potato Skins (haha)
        self.ship_anim_rate = 100
        self.potato_skins = [
                             pygame.image.load('images/potato_ship.png'),
                             pygame.image.load('images/potato_ship1.png'),
                             pygame.image.load('images/potato_ship2.png'),
                             pygame.image.load('images/potato_ship3.png'),
                             pygame.image.load('images/potato_ship4.png'),
                             pygame.image.load('images/potato_ship5.png'),
                             pygame.image.load('images/potato_ship6.png'),
                             pygame.image.load('images/potato_ship7.png'),
                             pygame.image.load('images/potato_ship8.png'),
                             pygame.image.load('images/potato_ship9.png'),
                             pygame.image.load('images/potato_ship10.png'),
                             pygame.image.load('images/potato_ship11.png'),
                             pygame.image.load('images/potato_ship12.png'),
                             ]

        # Bullet settings
        self.bullets_allowed = 6

        # Alien Bullet Settings
        self.a_bullet_width = 3
        self.a_bullet_height = 15
        self.a_bullet_color = (230, 230, 230)

        # Mini explosions
        self.mini_boom = [pygame.image.load('images/a1.png'),
                          pygame.image.load('images/a2.png'),
                          pygame.image.load('images/a3.png'),
                          pygame.image.load('images/a4.png')]

        # Alien settings
        self.alien_anim_rate = 300
        self.fleet_drop_speed = 1
        self.num_alien = 16
        # images and point values
        self.alien_type = {  # decided to switch 20  and 40
                           2: {'image': ('images/alien10.png',
                                         'images/alien10_2.png'),
                               'points': 10},
                           0: {'image': ('images/alien20.png',
                                         'images/alien20_2.png'),
                               'points': 40},
                           1: {'image': ('images/alien40.png',
                                         'images/alien40_2.png'),
                               'points': 20}
                           }

        # How quickly game spees up
        self.speedup_scale = 1.2

        # Clock
        self.clock = pygame.time.Clock()
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 6
        self.alien_speed_factor = 2
        self.a_bullet_speed_factor = 1.3
        self.a_bullet_rate = 500

        # fleet_direction of 1 represents right; -1 represetns left
        self.fleet_direction = 1

    def increase_speed(self):
        """increase speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.a_bullet_speed_factor *= self.speedup_scale
        self.a_bullet_rate *= self.speedup_scale
