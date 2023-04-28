from abilities.ability import Ability
import pygame
from pygame.math import Vector2 as Vector
from utils.math import snorm

class Cannonball(Ability):
    # Pop ability
    # Short version: add velocity, add invincibility circle/blue filter
    # Callback to stop velocity, add physics velocity so it gradually slows down
    def __init__(self, game, player, cooldown=0, key=pygame.K_e, duration=3000, speed=1000):
        super().__init__(game, player, cooldown, key, duration)
        self.speed = speed
    
    def pop(self):
        super().pop()
        mouse_pos = pygame.mouse.get_pos()
        self.player.phys_velocity = snorm(mouse_pos - self.player.position, self.speed)

    def on_ability_end(self):
        super().on_ability_end()
        self.player.phys_velocity += self.player.velocity
        self.player.velocity = Vector()