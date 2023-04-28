from abilities.ability import Ability
import pygame

class Cannonball(Ability):
    def __init__(self, game, cooldown, key=pygame.K_e, duration=3000):
        super().__init__(game, cooldown, key, duration)
        