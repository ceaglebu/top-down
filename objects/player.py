from abilities.reflect import Reflect
from abilities.roll import Roll
from utils.animation import AnimationData
import pygame
import sys
import os
from pygame.math import Vector2 as Vector
from game.settings import *
from game.event_timer import EventTimer, Timer
from utils.load_sprites import get_animation, get_image
from weapons.gun import PlayerShotgun, PlayerSemiAuto
from game.sounds import Sound
from .particle import *
from .moving_object import MovingObject


class Player(MovingObject):

    def __init__(self, group, game):
        # Initialize

        sprite_sheet = pygame.image.load(os.path.join(
            'assets', 'player', 'mPlayer_ [human].png')).convert_alpha()
        animations = {
            'idle': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 1, 0, 4, (11, 12)),
            'roll': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 6, 3, 5, (11, 12)),
            'run': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 2, 0, 8, (11, 12))
        }
        animation_data = AnimationData(animations, animations['idle'])
        super().__init__(group, game, animations['idle'][0], animation_data)

        self.gun = PlayerShotgun(
            gun_image= pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'shotgun.png')), .1 * PLAYER_SCALE).convert_alpha(),
            bullet_image= get_image(pygame.image.load(os.path.join('assets', 'misc', 'bullet.png')).convert_alpha(), (16,16), (8,8), PLAYER_SCALE * 4/5, (11,9), (5,4)).convert_alpha(),
            reload_time= RELOAD_TIME * 2, speed= BULLET_SPEED['player'],
            count=5, angle_range = (-10, 10),
            damage= 3,
            group= self.game.layers['accessories'], game= self.game, owner= self, 
            offset= Vector(4, 4) * PLAYER_SCALE)


        self.roll = Roll(game, self)
        self.ability = Reflect(game, self)
        self.abilities = [self.roll, self.ability]
        # self.gun = PlayerSemiAuto(
        #     gun_image= pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'shotgun.png')), .1 * PLAYER_SCALE).convert_alpha(),
        #     bullet_image= get_image(pygame.image.load(os.path.join('assets', 'misc', 'bullet.png')).convert_alpha(), (16,16), (8,8), PLAYER_SCALE * 4/5, (11,9), (5,4)).convert_alpha(),
        #     reload_time= RELOAD_TIME * 2, speed= BULLET_SPEED['player'],
        #     count=5, angle_range = (-10, 10),
        #     damage= 3,
        #     group= self.game.layers['accessories'], game= self.game, owner= self, 
        #     offset= Vector(4, 4) * PLAYER_SCALE)
        self.gun = PlayerSemiAuto(
            gun_image= pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'shotgun.png')), .1 * PLAYER_SCALE).convert_alpha(),
            bullet_image= get_image(pygame.image.load(os.path.join('assets', 'misc', 'bullet.png')).convert_alpha(), (16,16), (8,8), PLAYER_SCALE * 4/5, (11,9), (5,4)).convert_alpha(),
            reload_time= RELOAD_TIME, speed= BULLET_SPEED['player'],
            angle_range = (-10, 10),
            damage= 10,
            group= self.game.layers['accessories'], game= self.game, owner= self, 
            offset= Vector(4, 4) * PLAYER_SCALE)

        # State

        self.reload = True

    def handle_direction_input(self, dt):
        if self.game.mouse_pos[0] > self.rect.centerx:
            self.facing = 'right'
        else:
            self.facing = 'left'

        self.movement_control = Vector()

        if self.game.keys_down[pygame.K_w] or self.game.keys_down[pygame.K_UP]:
            self.movement_control.y = -1
        elif self.game.keys_down[pygame.K_s] or self.game.keys_down[pygame.K_DOWN]:
            self.movement_control.y = 1
        else:
            self.movement_control.y = 0

        if self.game.keys_down[pygame.K_d] or self.game.keys_down[pygame.K_RIGHT]:
            self.movement_control.x = 1
        elif self.game.keys_down[pygame.K_a] or self.game.keys_down[pygame.K_LEFT]:
            self.movement_control.x = -1
        else:
            self.movement_control.x = 0

        if self.movement_control.magnitude() != 0:
            self.movement_control = self.movement_control.normalize() * PLAYER_SPEED

    def shoot(self, dt):
        # Create bullet
        dir = self.game.mouse_pos - self.position
        self.gun.shoot(dir)
        self.game.sound.play(self.shoot_sound)

        # Handle recoil
        self.take_recoil(self.position - self.game.mouse_pos)

        # Handle reload
        self.reload = False

        def reload(self):
            self.reload = True
        self.game.timers.append(EventTimer(
            self.gun.reload_time * 1000, reload, self))
    
    def check_use_ability(self):
        for ability in self.abilities:
            if self.game.keys_down[ability.key]:
                ability.use()
    
    def hit(self, dir):
        is_hit = not self.roll.is_active
        if is_hit:
            self.take_knockback(dir)
            self.game.camera.shake()
        return is_hit

    def take_knockback(self, dir):
        self.phys_velocity += PLAYER_KNOCKBACK_STRENGTH * dir.normalize()

    def take_recoil(self, dir):
        self.phys_velocity += RECOIL_STRENGTH * dir.normalize()


    def think(self, dt):
        self.handle_direction_input(dt)

        self.check_use_ability()

        clicked = False
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        if (clicked or (self.game.mouse_buttons[0] and ENABLE_SPRAY)) and self.reload:
            self.shoot(dt)
        elif clicked and not self.reload:
            # play clicking sound effect
            pass

    def post_collision(self, dt, collision):
        (x_collision, y_collision) = collision
        if self.velocity.magnitude() == 0 or (not self.roll.is_active and ((x_collision and self.movement_control.x != 0 and self.movement_control.y == 0) or (y_collision and self.movement_control.y != 0 and self.movement_control.x == 0))):
            self.set_animation('idle')
        elif not self.roll.is_active and self.movement_control.magnitude() > 10:
            self.set_animation('run')

        self.gun.rect.center = self.position + self.gun.rect.offset
