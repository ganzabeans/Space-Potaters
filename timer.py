import pygame
from pygame import time


class Timer:

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.alien_rate = ai_settings.alien_anim_rate
        self.a_bullet_rate = ai_settings.a_bullet_rate
        self.ship_rate = ai_settings.ship_anim_rate

        self.current_time = 0
        self.alien_time = 0
        self.a_bullet_time = 0
        self.ship_time = 0
        self.ufo_time = 0
        self.ufo_rate = 10000

        self.alien_dict = {'time': self.alien_time,
                           'rate': self.alien_rate,
                           'switch': False}

        self.a_bullet_dict = {'time': self.a_bullet_time,
                              'rate': self.a_bullet_rate,
                              'switch': False}

        self.ship_dict = {'time': self.ship_time,
                          'rate': self.ship_rate,
                          'switch': False}

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.alien_dict['switch'] = self.update_times(self.alien_dict)
        self.a_bullet_dict['switch'] = self.update_times(self.a_bullet_dict)
        self.ship_dict['switch'] = self.update_times(self.ship_dict)

    def update_times(self, dict_type):
        """template to check if frame needs to swap"""
        if self.current_time - dict_type['time'] > dict_type['rate']:
            dict_type['time'] = self.current_time
            return True
        else:
            return False

    """
    def __init__(self, frames, wait=100, frameindex=0, step=1, looponce=False):
        # imagerect frames
        self.frames = frames
        self.wait = wait
        self.frameindex = frameindex
        self.step = step
        self.looponce = looponce
        self.finished = False
        self.lastframe = len(frames) - 1 if step == 1 else 0
        self.last = None

    def frame_index(self):
        now = pygame.time.get_ticks()
        if self.last is None:
            self.last = now
            self.frameindex = 0 if self.step == 1 else len(self.frames) - 1
            return 0
        elif not self.finished and now - self.last > self.wait:
            self.frameindex += self.step
            if self.looponce and self.frameindex == self.lastframe:
                self.finished = True
            else:
                self.frameindex %= len(self.frames)
            self.last = now
        return self.frameindex

    def reset(self):
        self.last = None
        self.finished = False

    def __str__(self): return 'Timer(frames=' + self.frames +\
                              ', wait=' + str(self.wait) + ', index=' +\
                              str(self.frameindex) + ')'

    def imagerect(self):
        return self.frames[self.frame_index()]
    """
