import math
from game.event_timer import EventTimer
from pygame.math import Vector2 as Vector
from utils.math import snorm
import pygame

class Ability:
    def __init__(self, game, cooldown, key=pygame.K_e):
        self.game = game
        self.cooldown = cooldown
        self.can_use = True
        self.key = key
    
    def reset_can_use(self):
        self.can_use = True
    
    def use(self):  
        if self.can_use:
            self.pop()
            self.can_use = False
            self.game.timers.append(EventTimer(self.cooldown, self.reset_can_use))
        else:
            # play failed ability sound?
            pass         

    def pop(self):        
        pass



class ReflectAbility(Ability):
    def __init__(self, game, cooldown=5000, dist_threshold=500):
        super().__init__(game, cooldown)
        self.dist_threshold = dist_threshold

    
    def pop(self):
        player = self.game.player
        p_center = player.rect.center
        for bullet in self.game.layers['bullets']:
            if bullet.gun.owner is not player:
                b_center = bullet.rect.center
                dist = math.dist(b_center, p_center)
                if dist <= self.dist_threshold:
                    bullet.gun = player.gun
                    bullet.velocity = snorm(bullet.position - player.position, bullet.gun.speed)

            