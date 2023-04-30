import pygame
from game.settings import *

class Timer:
    def __init__(self, time):
        self.active = False
        self.time = time
        self.start_time = 0

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.curr_time = self.start_time

    def deactivate(self):
        self.active = False
        self.start_time = 0
    
    def update(self, dt):
        self.curr_time += dt * 1000
        if self.active and self.curr_time - self.start_time >= self.time:
            self.deactivate()
            return False
        else:
            return True
    
    def time_left(self):
        return self.time - (self.curr_time - self.start_time)

    def percentage_done(self):
        return (self.curr_time - self.start_time) / self.time

class EventTimer(Timer):
    def __init__(self, time, function, args=None):
        super().__init__(time)
        self.function = function
        self.args = args
        self.activate()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.args != None:
            self.function(self.args)
        else:
            self.function()