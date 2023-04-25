from animation import AnimationData
import pygame
import sys
import os
from pygame.math import Vector2 as Vector
from settings import *
from event_timer import EventTimer, Timer
from load_sprites import get_animation
from child_rect import ChildRect
from bullet import Bullet
from gun import PlayerGun
from particle import *
from moving_object import MovingObject


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

        self.roll_particle_spawner = ParticleSpawner(group=self.game.layers['player-particles'],
                                                     position=(0, 0),
                                                     position_radius=5,
                                                     count=3,
                                                     color=((10, 10, 10)),
                                                     size_range=(10, 20),
                                                     velocity_range=(50, 100),
                                                     acceleration_strength_range=(
                                                         5, 7),
                                                     time_range=(.2, 1),
                                                     angle_range=(150, 390),
                                                     recallable=True)

        self.gun = PlayerGun(
            self.game.layers['accessories'], self.game, self, (20, 20))

        # State
        self.is_rolling = False
        self.can_roll = True
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

    def reset_roll(self):
        self.can_roll = True

    def end_roll(self):
        self.is_rolling = False
        self.collision_rect.height = self.rect.height * COLLISION_FORGIVENESS
        self.collision_rect.offset.y = self.collision_rect.default_offset.y
        if self.animation.active_animation == self.get_animation_by_key('roll'):
            self.set_animation('idle')

    def start_roll_particles(self):
        def spawn_roll_particles(self):
            if self.is_rolling:
                self.roll_particle_spawner.spawn(
                    4, self.collision_rect.midbottom)
                self.game.timers.append(EventTimer(
                    ROLL_PARTICLE_COOLDOWN * 1000, spawn_roll_particles, self))
        spawn_roll_particles(self)
        self.game.timers.append(EventTimer(
            ROLL_PARTICLE_COOLDOWN * 1000, spawn_roll_particles, self))

    def start_roll(self, dt):
        self.is_rolling = True
        self.can_roll = False
        self.collision_rect.height *= 3 / 4
        self.collision_rect.offset.y = int(
            (self.rect.bottom - self.collision_rect.bottom) * COLLISION_FORGIVENESS)
        self.set_animation('roll')
        self.start_roll_particles()

        self.game.timers.append(EventTimer(
            ROLL_COOLDOWN * 1000, self.reset_roll))

        self.game.timers.append(EventTimer(
            3 * 1000 / FRICTION_STRENGTH, self.end_roll))

        if self.movement_control.magnitude() != 0:
            self.phys_velocity += self.movement_control.normalize() * ROLL_STRENGTH

    def shoot(self, dt):
        # Create bullet
        dir = self.game.mouse_pos - self.position
        self.gun.shoot(dir)

        # Handle recoil
        self.phys_velocity += RECOIL_STRENGTH * \
            (self.position - self.game.mouse_pos).normalize()

        # Handle reload
        self.reload = False

        def reload(self):
            self.reload = True
        self.game.timers.append(EventTimer(
            RELOAD_TIME * 1000, reload, self))

    def think(self, dt):
        self.handle_direction_input(dt)
        can_really_roll = self.can_roll and self.phys_velocity.magnitude(
        ) <= 500 and self.movement_control.magnitude() != 0

        if self.game.keys_down[pygame.K_SPACE] and can_really_roll:
            self.start_roll(dt)

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
        if self.velocity.magnitude() == 0 or (not self.is_rolling and ((x_collision and self.movement_control.x != 0 and self.movement_control.y == 0) or (y_collision and self.movement_control.y != 0 and self.movement_control.x == 0))):
            self.set_animation('idle')
        elif not self.is_rolling and self.movement_control.magnitude() > 10:
            self.set_animation('run')

        self.gun.rect.center = self.position + self.gun.rect.offset
