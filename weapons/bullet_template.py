import pygame
import random as r
from weapons.bullet import Bullet
from utils.math import *

# Modular way to change what bullets a gun will shoot
# Can create different kinds for specific use cases
class AmmoTemplate():
    def __init__(self, bullet_image, reload_time):
        self.bullet_image = bullet_image
        self.reload_time = reload_time

    def instantiate(self, layer, game, gun, dir):
        # do whatever funky stuff you want to do when gun is shot
        pass


class BulletTemplate(AmmoTemplate):
    def __init__(self, bullet_image, reload_time, speed, count, angle_range, damage):
        super().__init__(bullet_image, reload_time)
        self.speed = speed
        self.count = count
        self.angle_range = angle_range
        self.damage = damage

    def instantiate(self, layer, game, gun, dir): 
        for _ in range(self.count):
            angle = r.uniform(*self.angle_range) + Vector().angle_to(Vector(*dir))
            # print(dir, vector_to_angle(dir))
            # final_dir = angle_to_vector(angle)
            Bullet(self.bullet_image, layer, game, gun, self.damage,
                gun.get_endpoint(), snorm(angle_to_vector(angle), self.speed))

class LaserTemplate():
    def __init__(self):
        pass




