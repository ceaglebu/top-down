import pygame
from objects.particle import Particle
from pygame.math import Vector2 as Vector
from game.settings import *
import random as rand
from game.event_timer import EventTimer

class SpriteGroup3d(pygame.sprite.Group):
    def __init__(self, z):
        super().__init__()
        self.z = z

    def empty(self):
        self.spritedict = {}

class CameraGroup:
    def __init__(self, game):
        self.game = game
        self.offset = Vector(0,0)
        self.is_shaking = False
        self.shake_offset = Vector()
        self.shake_intensity = CAMERA_SHAKE_INTENSITY
    
    def update(self, dt):
        # apply offset
        mouse = pygame.mouse.get_pos()
        
        self.mouse_offset = (Vector(mouse) - Vector(WIN_WIDTH / 2, WIN_HEIGHT / 2)) * -.3

        self.player_offset = -self.game.player.position + Vector(WIN_WIDTH, WIN_HEIGHT) / 2

        if self.is_shaking:
            self.shake_offset += Vector(rand.randint(-self.shake_intensity,self.shake_intensity) * dt, rand.randint(-self.shake_intensity,self.shake_intensity) * dt)
        else:
            if self.shake_offset.magnitude() > 2:
                self.shake_offset -= self.shake_offset * 2 * dt
            elif self.shake_offset.magnitude() > 0:
                self.shake_offset = Vector()

        self.offset = self.mouse_offset + self.shake_offset + self.player_offset

    
    def shake(self, intensity = CAMERA_SHAKE_INTENSITY, length = 150):
        if self.is_shaking:
            self.shake_intensity = max(self.shake_intensity, intensity)
        else:
            self.is_shaking = True
            self.shake_intensity = intensity
            def end_shake(self):
                self.is_shaking = False
            self.game.timers.append(EventTimer(length, end_shake, self))

    def draw(self):
        
        self.game.screen.fill(BACKGROUND_COLOR)
        
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
                    if object.position.x + self.offset.x > 0:
                        pygame.draw.circle(self.game.screen, object.color, object.position + self.offset, object.size / 2)