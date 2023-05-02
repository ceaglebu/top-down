from utils.animation import AnimationData
from game.event_timer import EventTimer
from weapons.gun import EnemyGun
from utils.load_sprites import get_animation, get_image
from game.sounds import Sound
from game.settings import *
import os
import pygame
from pygame.math import Vector2 as Vector
from ..particle import *
from ..moving_object import MovingObject


class Enemy(MovingObject):
    def __init__(self, group, game, animations, gun, health=100, start_pos=(0,0)):

        animation_data = AnimationData(animations, animations['idle'])

        super().__init__(group, game, animations['idle'][0], animation_data, start_pos, collision_forgiveness=ENEMY_COLLISION_FORGIVENESS, damage_forgiveness=ENEMY_DAMAGE_FORGIVENESS)

        self.health = health
        self.is_alive = True
        
        self.gun = gun

    def think(self, dt):
        pass

    def post_collision(self, dt, collide):
        self.gun.rect.center = self.position + self.gun.rect.offset

    def take_damage(self, damage):
        if self.is_alive:
            self.health -= damage
            if self.health <= 0:
                self.die()
    
    def red_highlight(self):
        self.image.set_colorkey((0, 0, 0))
        mask = pygame.mask.from_surface(self.image)
        self.image.blit(mask.to_surface(unsetcolor=(
            0, 0, 0, 0), setcolor=(255, 0, 0, 50)), (0, 0))

    def slowmo_before_death(self, time, on_death):
        self.game.start_bullet_time(50)
        self.game.timers.append(EventTimer(50, on_death, self))

    def die(self):
        def death_explosion(self):
            ParticleSpawner(group=self.game.layers['particles'],
                            position=self.rect.center,
                            position_radius=30,
                            count=20,
                            color='yellow',
                            size_range=(10, 50),
                            velocity_range=(200, 2500),
                            acceleration_strength_range=(5, 15),
                            time_range=(.2, 1),
                            angle_range=(0, 360))
            self.gun.kill()
            self.kill()
            self.game.camera.shake(intensity=ENEMY_DIES_SHAKE_INTENSITY)
            self.game.sound.play(Sound('enemy_death', VOLUME /2 ))
        self.is_alive = False

        death_time = 20
        self.red_highlight()
        if len(self.group) == 1:
            death_time *= 4
            self.game.start_bullet_time(death_time)
        self.game.timers.append(EventTimer(death_time, death_explosion, self))

    def update(self, dt):
        if self.is_alive:
            super().update(dt)