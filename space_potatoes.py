# Anisha Braganza
# Space Potatoes

import pygame
from pygame.sprite import Group
from ufo import Ufo
from settings import Settings
from game_stats import GameStats
from background import Background
from timer import Timer
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bunker import Bunker
from alien import Alien
from mini_boom import Mini_Boom
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Potaters")

    # Make buttons
    play_button = Button(ai_settings, screen, 'play')
    high_score_button = Button(ai_settings, screen, 'hs')
    back_button = Button(ai_settings, screen, 'back')

    # Create background
    background = Background(ai_settings, screen)

    # Create instance to store game states and create scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #  Make a ship.
    ship = Ship(ai_settings, screen)

    # Make group to store bullets
    bullets = Group()
    # Make alien group
    aliens = Group()
    # Made group to store alien bullets
    a_bullets = Group()

    # Create alien fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create timer
    timer = Timer(ai_settings)

    # create ufo
    ufo = Ufo(ai_settings, screen)

    # Create explosion group
    kabooms = Group()

    # Make a bunker
    bunker = Group()

    background.blitme()

    # start main game loop
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets, a_bullets, background, bunker,
                        high_score_button, back_button)

        if stats.game_active:
            timer.update()
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets, a_bullets, bunker, kabooms, ufo)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             bullets, a_bullets, bunker, timer)
            gf.update_a_bullets(ai_settings, screen, stats, sb, ship, aliens,
                                bullets, a_bullets, bunker, timer)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         a_bullets, play_button, timer, bunker, background,
                         high_score_button, back_button, kabooms, ufo)


run_game()
