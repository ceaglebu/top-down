import pygame,os
from game.settings import *
from utils.load_sprites import get_animation, get_image
from weapons.gun import EnemyGun
from objects.enemies import Enemy
from pygame.math import Vector2 as Vector
from game.event_timer import EventTimer
import math

class Sniper(Enemy):
    def __init__(self, group, game, start_pos, health=30):
        # Load sprite sheet
        sprite_sheet = pygame.image.load(os.path.join(
            'assets', 'player', 'mPlayer_ [human].png')).convert_alpha()

        # Define animations
        animations = {
            'idle': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 1, 0, 4, (11, 12)),
            'aim': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 6, 3, 5, (11, 12)),
            'run': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 2, 0, 8, (11, 12))
        }

        self.game = game

        # Initialize with a more powerful but slower gun
        super().__init__(group, game, animations, \
                         EnemyGun(
                            gun_image= pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'shotgun.png')), .15 * PLAYER_SCALE).convert_alpha(),  # Slightly larger scale
                            bullet_image= get_image(pygame.image.load(os.path.join('assets', 'misc', 'bullet.png')).convert_alpha(), (16,16), (8,8), PLAYER_SCALE * 4/5, (11,9), (5,4)).convert_alpha(),
                            speed = BULLET_SPEED['enemy'] * 1.5,  # Faster bullets
                            damage = 25,  # More damage
                            group= self.game.layers['accessories'], game= self.game, owner= self, 
                            offset= Vector(4, 4) * PLAYER_SCALE),
                            health = health, start_pos=start_pos)
    
        self.can_act = True
        self.can_attack = False
        self.aiming = False
        self.aim_time = 0
        self.max_aim_time = 1000  # 1 second aim time

        # Longer attack cooldown for balance
        self.game.timers.append(EventTimer(ENEMY_ATTACK * 2, self.reset_attack))

    def think(self, dt):
        if self.can_act:
            player_pos = self.game.player.position
            distance = (player_pos - self.position).magnitude()
            
            if distance < 300:  # If player is too close, run away
                self.run_away()
            elif distance > 500:  # If player is too far, move closer
                self.move_towards_player()
            else:  # If in optimal range, aim and shoot
                self.aim_and_shoot()
            
            self.can_act = False
            self.game.timers.append(EventTimer(ENEMY_ACTION * 1000, self.reset_action))

    def run_away(self):
        player_pos = self.game.player.position
        dir = Vector(self.position - player_pos)
        if dir.magnitude() != 0:
            self.phys_velocity += dir.normalize() * ENEMY_SPEED * 0.8  # Slightly slower than normal
        self.set_animation('run')
        if dir[0] < 0:
            self.facing = 'left'
        else:
            self.facing = 'right'

    def move_towards_player(self):
        player_pos = self.game.player.position
        dir = Vector(player_pos - self.position)
        if dir.magnitude() != 0:
            self.phys_velocity += dir.normalize() * ENEMY_SPEED * 0.6  # Even slower movement
        self.set_animation('run')
        if dir[0] < 0:
            self.facing = 'left'
        else:
            self.facing = 'right'

    def aim_and_shoot(self):
        if not self.aiming:
            self.aiming = True
            self.aim_time = 0
            self.set_animation('aim')
            self.phys_velocity = Vector()  # Stop moving while aiming
        
        self.aim_time += ENEMY_ACTION * 1000
        
        if self.aim_time >= self.max_aim_time and self.can_attack:
            self.attack()
            self.aiming = False
            self.set_animation('idle')

    def attack(self):
        dir = self.game.player.position - self.position
        self.gun.shoot(dir)
        self.can_attack = False
        self.game.timers.append(EventTimer(ENEMY_ATTACK * 2 * 1000, self.reset_attack))

    def reset_action(self):
        self.can_act = True

    def reset_attack(self):
        self.can_attack = True 