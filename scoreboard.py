import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    """A class to report scoring information"""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.ufo_score = False

        # Font settings
        self.text_color = self.ai_settings.text_color
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial and high score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.hs_list = [self.font.render("High Scores:", True,
                                         self.text_color)]
        self.hs_list_set = False

    def prep_score(self):
        """Turn score into a rendred image"""
        round_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(round_score)
        self.score_image = self.font.render("Score: " + score_str, True,
                                            self.text_color)

        # Display current score at top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high schore into a rendered image"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color)

        # Center high score at top of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        if self.ufo_score:
            self.screen.blit(self.ufo_image, self.ufo_position)

    def prep_level(self):
        """Turn the level into a rendered image"""
        self.level_image = self.font.render("Level: " + str(self.stats.level),
                                            True, self.text_color)

        # position level below score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_hs(self):
        """prep high socre to show
        skips if already has been prepped """
        if not self.hs_list_set:
            self.hs_list_set = True
            for n in range(len(self.stats.hs_list)):
                self.hs_list.append(self.font.render(" " +
                                    self.stats.hs_list[n], True,
                                    self.text_color))

    def display_high_scores(self):
        """displays high score"""
        for n in range(len(self.hs_list)):
            self.screen.blit(self.hs_list[n], (500, 100 + 50*n))

    def ufo_points(self, points, position):
        """displays points for hit ufo"""
        ufo_str = "{:,}".format(points)
        self.ufo_position = position
        print(self.ufo_position)
        self.ufo_image = self.font.render(ufo_str, True, (255, 0, 0))
        self.ufo_score = True

    def display_end_score(self):
        # Display player score at end
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("High Score: " +
                                                 high_score_str, True,
                                                 self.text_color)
        self.screen.blit(self.high_score_image, (450, 150))
        self.screen.blit(self.score_image, (500, 250))
