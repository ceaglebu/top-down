import pygame,os,math
from child_rect import ChildRect
from pygame.math import Vector2 as Vector
from game_object import GameObject
from utils import rot_center

class Gun(GameObject):

    def __init__(self, group, game, owner, offset = Vector(0,0)):
        default_image = pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'shotgun.png')), .5).convert_alpha()
        super().__init__(group, game, default_image, start_pos=Vector(default_image.get_rect().center))
        
        self.owner = owner
        self.offset = offset
        self.rect = ChildRect(self.image.get_rect(), offset)
    
    def get_endpoint(self):
        endpoint = Vector()
        endpoint.x = self.rect.centerx + self.default_image.get_rect().width//2 * math.cos(math.radians(self.angle))
        endpoint.y = self.rect.centery - self.default_image.get_rect().width//2 * math.sin(math.radians(self.angle))
        return endpoint
    
    def point(self):
        pass
    
    def shoot(self, dir):
        pass

    def update(self, dt):
        self.point()

class PlayerGun(Gun):
    def __init__(self, group, game, owner, offset=Vector(0, 0)):
        super().__init__(group, game, owner, offset)
    
    def point(self):
        mouse_pos = self.game.mouse_pos
        if mouse_pos[1] != self.owner.position.y:
            rotate_angle = math.degrees(math.atan(((abs(mouse_pos[0] - self.owner.position.x)) / (mouse_pos[1] - self.owner.position.y))))
        else:
            rotate_angle = 90
        if mouse_pos[1] - self.owner.position.y < 0:
            rotate_angle += 180
        rotate_angle -= 90
        self.image, self.rect = rot_center(self.default_image, rotate_angle, self.rect.centerx, self.rect.centery)
        if self.owner.facing == 'left':
            self.flip = -1
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        else:
            self.flip = 1
        self.rect = ChildRect(self.rect, (self.offset[0] * self.flip, self.offset[1]))

        self.angle = -self.flip * (90 - self.flip * 90 - rotate_angle)
        self.position = Vector(self.rect.center)
    
    def shoot(self, dir):
        pass


class EnemyGun(Gun):

    def __init__(self, group, game, owner, offset=Vector(0, 0)):
        super().__init__(group, game, owner, offset)


    def point(self):
        if self.game.player.position[1] != self.owner.position.y:
            rotate_angle = math.degrees(math.atan(((abs(self.game.player.position[0] - self.owner.position.x)) / (self.game.player.position[1] - self.owner.position.y))))
        else:
            rotate_angle = 90
        if self.game.player.position[1] - self.owner.position.y < 0:
            rotate_angle += 180
        rotate_angle -= 90
        self.image, self.rect = rot_center(self.default_image, rotate_angle, self.rect.centerx, self.rect.centery)
        if self.owner.facing == 'left':
            self.flip = -1
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        else:
            self.flip = 1
        self.rect = ChildRect(self.rect, (self.offset[0] * self.flip, self.offset[1]))
        self.position = Vector(self.rect.center)
    
    def shoot(self):
        pass

