from objects.particle import ParticleSpawner
import pygame,os,math
from objects.child_rect import ChildRect
from pygame.math import Vector2 as Vector
from objects.game_object import GameObject
from game.settings import BULLET_SPEED
from utils.math import rot_center, snorm
from weapons.bullet import Bullet
from game.settings import *

class Gun(GameObject):

    def __init__(self, bullet_speed, group, game, owner, offset = Vector(0,0)):
        default_image = pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'shotgun.png')), .1 * PLAYER_SCALE).convert_alpha()
        super().__init__(group, game, default_image, start_pos=Vector(default_image.get_rect().center))
        
        self.bullet_speed = bullet_speed
        self.owner = owner
        self.offset = offset
        self.rect = ChildRect(self.image.get_rect(), offset)
    
    def get_endpoint(self):
        endpoint = Vector()
        endpoint.x = self.rect.centerx + self.default_image.get_rect().width//2 * math.cos(math.radians(self.angle))
        endpoint.y = self.rect.centery - self.default_image.get_rect().width//2 * math.sin(math.radians(self.angle))
        return endpoint
    
    def point(self, toward=Vector()):
        dir = toward - self.owner.position
        if dir[1] != 0:
            rotate_angle = math.degrees(math.atan(abs(dir[0]) / dir[1]))
        else:
            rotate_angle = 90

        if dir[1] < 0:
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
        # Create bullet
        Bullet(self.game.layers['bullets'], self.game, self,
               self.get_endpoint(), snorm(dir, self.bullet_speed))

    def update(self, dt):
        self.point()

class PlayerGun(Gun):
    def __init__(self, bullet_speed, group, game, owner, offset=Vector(0, 0)):
        super().__init__(bullet_speed, group, game, owner, offset)
    
    def point(self):
        super().point(self.game.mouse_pos)
    
    def shoot(self, dir):
        super().shoot(dir)
        ParticleSpawner(group=self.game.layers['particles'],
                        position=self.get_endpoint(),
                        position_radius=5,
                        count=3,
                        color='yellow',
                        size_range=(1, 10),
                        velocity_range=(200, 1500),
                        acceleration_strength_range=(5, 15),
                        time_range=(.2, 1),
                        angle_range=(self.angle - 30, self.angle + 30))


class EnemyGun(Gun):

    def __init__(self, bullet_speed, group, game, owner, offset=Vector(0, 0)):
        super().__init__(bullet_speed, group, game, owner, offset)


    def point(self):
        super().point(self.game.player.position)

