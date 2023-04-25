from bullet import Bullet
from event_timer import EventTimer
from gun import EnemyGun
from load_sprites import get_animation
from settings import *
import os
import pygame
from pygame.math import Vector2 as Vector
from child_rect import ChildRect
from particle import *
from moving_object import MovingObject


class Enemy(MovingObject):
    def __init__(self, group, game):

        sprite_sheet = pygame.image.load(os.path.join(
            'assets', 'player', 'mPlayer_ [human].png')).convert_alpha()

        animations = {
            'idle': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 1, 0, 4, (11, 12)),
            'run': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 6, 3, 5, (11, 12)),
            'attack': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 2, 0, 8, (11, 12))
        }

        super().__init__(group, game, animations, animations['idle'])

        self.health = 100
        self.alive = True

        self.gun = EnemyGun(
            self.game.layers['accessories'],  game, owner=self, offset=(20, 15))
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
        self.health -= damage
        if self.health <= 0:
            self.die()

    def reset_attack(self):
        self.can_attack = True

    def attack(self):
        dir = (self.game.player.position - self.position).normalize()
        Bullet(self, self.game.layers['bullets'],
               self.gun.get_endpoint(), dir * BULLET_SPEED)

        # Handle reload
        self.can_attack = False

        self.game.timers.append(EventTimer(ENEMY_ATTACK * 1000, self.reset_attack))
    
    def red_highlight(self):
        self.image.set_colorkey((0, 0, 0))
        mask = pygame.mask.from_surface(self.image)
        self.image.blit(mask.to_surface(unsetcolor=(
            0, 0, 0, 0), setcolor=(255, 0, 0, 50)), (0, 0))

    def slowmo_before_death(self, time, on_death):
        self.game.start_bullet_time(time)
        self.game.timers.append(EventTimer(time, on_death, self))

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
        self.alive = False

        self.red_highlight()
        self.slowmo_before_death(200, death_explosion)

    def update(self, dt):
        if self.alive:
            super().update(dt)
