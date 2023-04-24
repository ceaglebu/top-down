import pygame
from particle import Particle

class SpriteGroup3d(pygame.sprite.Group):
    def __init__(self, z):
        super().__init__()
        self.z = z

class CameraGroup:
    def __init__(self, game):
        self.game = game

    def draw(self):
        prev = None
        layer_list = {}
        for layer in self.game.layers.values():
            z_vals = layer_list.keys()
            if layer.z in z_vals:
                layer_list[layer.z] += layer.sprites()
            else:
                layer_list[layer.z] = layer.sprites()

        for z in layer_list.values():
            def myfunc(o):
                return o.position[1]
            z.sort(key=myfunc)

            for object in z:
                if isinstance(object, pygame.sprite.Sprite):
                    self.game.screen.blit(object.image, object.rect.topleft)
                elif isinstance(object, Particle):
                    if object.position.x > 0:
                        pygame.draw.circle(self.game.screen, object.color, object.position, object.size / 2)

        # Go through every item and draw it correctly
        

        # apply offset
        
        pass