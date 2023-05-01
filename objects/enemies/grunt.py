import pygame,os
from game.settings import *
from utils.load_sprites import get_animation, get_image
from weapons.gun import EnemyGun
from objects.enemies import Enemy
from pygame.math import Vector2 as Vector
from game.event_timer import EventTimer


class Grunt(Enemy):
    def __init__(self, group, game, start_pos, health=50):

        sprite_sheet = pygame.image.load(os.path.join(
            'assets', 'player', 'mPlayer_ [human].png')).convert_alpha()

        animations = {
            'idle': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 1, 0, 4, (11, 12)),
            'attack': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 6, 3, 5, (11, 12)),
            'run': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 2, 0, 8, (11, 12))
        }

        self.game = game

        super().__init__(group, game, animations, \
                         EnemyGun(
                            gun_image= pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'shotgun.png')), .1 * PLAYER_SCALE).convert_alpha(),
                            bullet_image= get_image(pygame.image.load(os.path.join('assets', 'misc', 'bullet.png')).convert_alpha(), (16,16), (8,8), PLAYER_SCALE * 4/5, (11,9), (5,4)).convert_alpha(),
                            speed = BULLET_SPEED['enemy'],
                            damage = 10,
                            group= self.game.layers['accessories'], game= self.game, owner= self, 
                            offset= Vector(4, 4) * PLAYER_SCALE),
                            health = health, start_pos=start_pos)
    
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

    def reset_attack(self):
        self.can_attack = True

    def attack(self):
        dir = self.game.player.position - self.position
        self.gun.shoot(dir)

        # Handle reload
        self.can_attack = False

        self.game.timers.append(EventTimer(ENEMY_ATTACK * 1000, self.reset_attack))

    def update(self, dt):
        if self.is_alive:
            super().update(dt)