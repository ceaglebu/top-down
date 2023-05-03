import pygame
from behaviors.behavior import Behavior

class PlayerDefaultBehavior(Behavior):
    def __init__(self, game, owner):
        super().__init__(game, owner)