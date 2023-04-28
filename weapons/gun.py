from objects.particle import ParticleSpawner
import pygame,os,math
from objects.child_rect import ChildRect
from pygame.math import Vector2 as Vector
from objects.game_object import GameObject
from game.settings import BULLET_SPEED
from utils.math import rot_center, snorm, angle_to_vector
from weapons.bullet import Bullet
from game.settings import *
from utils.load_sprites import get_image
from game.event_timer import EventTimer
import random as rand

class Gun(GameObject):

    def __init__(self, gun_image, bullet_image, group, game, owner, offset = Vector(0,0)):
        default_image = gun_image
        super().__init__(group, game, default_image, start_pos=Vector(default_image.get_rect().center))
    
        self.owner = owner
        self.offset = offset
        self.rect = ChildRect(self.image.get_rect(), offset)

        self.bullet_image = bullet_image
    
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
        pass

    def update(self, dt):
        self.point()

class PlayerGun(Gun):
    
    def __init__(self, gun_image, bullet_image, group, game, owner, offset=Vector(0, 0)):
        super().__init__(gun_image, bullet_image, group, game, owner, offset)
    
    def point(self):
        super().point(self.game.mouse_pos)
    
    def shoot(self, dir):
        super().shoot(dir)
        self.game.camera.shake(intensity=500, length = .05)
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
        

class PlayerSemiAuto(PlayerGun):

    def __init__(self, gun_image, bullet_image, reload_time, speed, angle_range, damage, group, game, owner, offset=Vector()):
        super().__init__(gun_image, bullet_image, group, game, owner, offset)
        self.reload_time = reload_time
        self.speed = speed
        self.angle_range = angle_range
        self.damage = damage

    def shoot(self, dir):
        super().shoot(dir)
        angle = rand.uniform(*self.angle_range) + Vector().angle_to(Vector(*dir))
        Bullet(self.bullet_image, self.game.layers['bullets'], self.game, self, self.damage, 
            self.get_endpoint(), snorm(angle_to_vector(angle), self.speed))

class PlayerShotgun(PlayerGun):

    def __init__(self, gun_image, bullet_image, reload_time, speed, count, angle_range, damage, group, game, owner, offset=Vector()):
        super().__init__(gun_image, bullet_image, group, game, owner, offset)
        self.reload_time = reload_time
        self.speed = speed
        self.count = count
        self.angle_range = angle_range
        self.damage = damage
    
    def shoot(self, dir):
        super().shoot(dir)
        for i in range(self.count):
            angle = self.angle_range[0] + i * ((self.angle_range[1] - self.angle_range[0]) / self.count) \
                + Vector().angle_to(Vector(*dir))
            Bullet(self.bullet_image, self.game.layers['bullets'], self.game, self, self.damage,
                self.get_endpoint(), snorm(angle_to_vector(angle), self.speed))



class EnemyGun(Gun):
    def __init__(self, gun_image, bullet_image, speed, damage, group, game, owner, offset=Vector()):
        super().__init__(gun_image, bullet_image, group, game, owner, offset)
        self.damage = damage
        self.speed = speed

    def point(self):
        super().point(self.game.player.position)
    
    def shoot(self, dir):
        Bullet(self.bullet_image, self.game.layers['bullets'], self.game, self, self.damage, 
            self.get_endpoint(), snorm(dir, self.speed))


