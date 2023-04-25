import pygame
from pygame.math import Vector2 as Vector

class GameObject(pygame.sprite.Sprite):
    def __init__(self, group, game, default_image, start_pos=Vector(), angle=0, flip=1):
        super().__init__(group)
        self.game = game
        self.default_image = default_image
        self.image = pygame.transform.rotate(self.default_image, 0)
        self.rect = self.image.get_rect()
        self.position = start_pos

        self.angle = angle
        self.flip = flip
    
    def update(self, dt):
        pass