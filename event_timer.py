import pygame
from settings import *

class Timer:
    def __init__(self, time):
        self.active = False
        self.time = time
        self.start_time = 0

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
    
    def update(self):
        curr_time = pygame.time.get_ticks()
        if self.active and curr_time - self.start_time >= self.time:
            self.deactivate()

class EventTimer(Timer):
    def __init__(self, time, function, args=None):
        super().__init__(time)
        self.function = function
        self.args = args
        self.activate()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        self.function(self.args)