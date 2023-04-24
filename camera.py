import pygame
from particle import Particle
from pygame.math import Vector2 as Vector
from settings import *

class SpriteGroup3d(pygame.sprite.Group):
    def __init__(self, z):
        super().__init__()
        self.z = z

class CameraGroup:
    def __init__(self, game):
        self.game = game
        self.offset = Vector(0,0)
    
    def update(self, dt):
        # apply offset
        mouse = pygame.mouse.get_pos()
        
        self.mouse_offset = (Vector(mouse) - Vector(WIN_WIDTH / 2, WIN_HEIGHT / 2)) * -.03

        self.offset = self.mouse_offset

    def draw(self):
        # Go through every item and draw it correctly
        layer_list = {}
        for layer in self.game.layers.values():
            z_vals = layer_list.keys()
            if layer.z in z_vals:
                layer_list[layer.z] += layer.sprites()
            else:
                layer_list[layer.z] = layer.sprites()

        for z in layer_list.values():
            if z and not isinstance(z[0], Particle):
                z.sort(key=lambda o: o.position[1])

            for object in z:
                if isinstance(object, pygame.sprite.Sprite):
                    self.game.screen.blit(object.image, Vector(object.rect.topleft) + self.offset)
                elif isinstance(object, Particle):
                    if object.position.x > 0:
                        pygame.draw.circle(self.game.screen, object.color, object.position + self.offset, object.size / 2)