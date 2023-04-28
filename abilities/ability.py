from game.event_timer import EventTimer
import pygame


class Ability:
    def __init__(self, game, cooldown, key=pygame.K_e, duration=0):
        self.game = game
        self.cooldown = cooldown
        self.can_use = True
        self.is_active = False
        self.key = key
        self.duration = duration

    def reset_can_use(self):
        self.can_use = True
    
    def on_ability_end(self):
        self.is_active = False

    def can_pop(self):
        return self.can_use

    def use(self):
        if self.can_pop():
            if self.cooldown != 0:
                self.can_use = False
                self.game.timers.append(EventTimer(
                    self.cooldown, self.reset_can_use))
            if self.duration != 0:
                self.is_active = True
                self.game.timers.append(EventTimer(self.duration, self.on_ability_end))
            self.pop()
        else:
            # play failed ability sound?
            pass

    def pop(self):
        pass