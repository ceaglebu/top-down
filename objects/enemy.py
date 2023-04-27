from utils.animation import AnimationData
from game.event_timer import EventTimer
from weapons.gun import EnemyGun
from utils.load_sprites import get_animation, get_image
from game.settings import *
import os
import pygame
from pygame.math import Vector2 as Vector
from .particle import *
from .moving_object import MovingObject


class Enemy(MovingObject):
    def __init__(self, group, game):

        sprite_sheet = pygame.image.load(os.path.join(
            'assets', 'player', 'mPlayer_ [human].png')).convert_alpha()

        animations = {
            'idle': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 1, 0, 4, (11, 12)),
            'attack': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 6, 3, 5, (11, 12)),
            'run': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 2, 0, 8, (11, 12))
        }
        animation_data = AnimationData(animations, animations['idle'])

        super().__init__(group, game, animations['idle'][0], animation_data)

        self.health = 100
        self.is_alive = True
        
        self.gun = EnemyGun(
            gun_image= pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'shotgun.png')), .1 * PLAYER_SCALE).convert_alpha(),
            bullet_image= get_image(pygame.image.load(os.path.join('assets', 'misc', 'bullet.png')).convert_alpha(), (16,16), (8,8), PLAYER_SCALE * 4/5, (11,9), (5,4)).convert_alpha(),
            speed = BULLET_SPEED['enemy'],
            damage = 1,
            group= self.game.layers['accessories'], game= self.game, owner= self, 
            offset= Vector(4, 4) * PLAYER_SCALE)
    
        self.can_act = True
        self.can_attack = False

        self.game.timers.append(EventTimer(ENEMY_ATTACK, self.reset_attack))

    def ai_move(self):
        player_pos = self.game.player.position
        dir = Vector(
            player_pos - self.position)

        if dir.magnitude() != 0:
            self.phys_velocity += dir.normalize() * ENEMY_SPEED
        if dir[0] < 0:
            self.facing = 'left'
        else:
            self.facing = 'right'

    def think(self, dt):
        if self.can_act:
            if self.can_attack:
                self.attack()
            else:
                self.ai_move()
            self.can_act = False

            def reset(self):
                self.can_act = True
            self.game.timers.append(EventTimer(
                ENEMY_ACTION * 1000, reset, self))

    def post_collision(self, dt, collide):
        self.gun.rect.center = self.position + self.gun.rect.offset

    def take_damage(self, damage):
        if self.is_alive:
            self.health -= damage
            if self.health <= 0:
                self.die()

    def reset_attack(self):
        self.can_attack = True

    def attack(self):
        dir = self.game.player.position - self.position
        self.gun.shoot(dir)

        # Handle reload
        self.can_attack = False

        self.game.timers.append(EventTimer(ENEMY_ATTACK * 1000, self.reset_attack))
    
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
        self.is_alive = False

        self.red_highlight()
        self.slowmo_before_death(700, death_explosion)

    def update(self, dt):
        if self.is_alive:
            super().update(dt)
