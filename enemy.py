from bullet import Bullet
from event_timer import EventTimer
from gun import EnemyGun
from load_sprites import get_animation
from settings import ANIMATION_TILESIZE, BULLET_SPEED, ENEMY_ACTION, ENEMY_ATTACK, PLAYER_SCALE, COLLISION_FORGIVENESS, ANIMATION_FRAMERATE, FRICTION_STRENGTH, RELOAD_TIME, WIN_HEIGHT, WIN_WIDTH, ENEMY_SPEED
import os
import pygame
from pygame.math import Vector2 as Vector
from child_rect import ChildRect
from particle import * 


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, game):
        super().__init__(group)

        self.game = game
        self.screen = pygame.display.get_surface()

        self.position = Vector((0, 0))
        self.velocity = Vector((0, 0))
        self.phys_velocity = Vector((0, 0))
        self.phys_acceleration = Vector((0, 0))

        self.start_time = pygame.time.get_ticks()
        sprite_sheet = pygame.image.load(os.path.join(
            'assets', 'player', 'mPlayer_ [human].png')).convert_alpha()

        self.animations = {
            'idle': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 1, 0, 4, (11, 12)),
            'run': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 6, 3, 5, (11, 12)),
            'attack': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11, 16), PLAYER_SCALE, 2, 0, 8, (11, 12))
        }

        self.active_animation = self.animations['idle']
        self.anim_frame = 0
        self.facing = 'right'
        self.image = self.active_animation[self.anim_frame]
        self.rect = self.image.get_rect()
        self.rect.center = ((0, 0))

        self.health = 100
        self.timers = []
        self.child_rects = []
        self.collision_rect = ChildRect(pygame.Rect(self.rect.center, (0, 0)).inflate(Vector(
            self.rect.size) * COLLISION_FORGIVENESS), (0, int(self.rect.height - COLLISION_FORGIVENESS * self.rect.height) / 2))
        self.child_rects.append(self.collision_rect)

        self.gun = EnemyGun(self, game, self.game.layers['accessories'], (20, 15))
        self.can_act = True
        self.can_attack = True
    
    def ai_move(self):
        player_pos = self.game.player.position
        self.movement_control = Vector(
            player_pos.x - self.position.x, player_pos.y - self.position.y)

        if self.movement_control.magnitude() != 0:
            self.movement_control = self.movement_control.normalize() * ENEMY_SPEED

    def think(self, dt):
        self.movement_control = Vector()
        if self.can_act:
            if self.can_attack:
                self.attack()
            else:
                self.ai_move()
            self.can_act = False
            def reset(self):
                self.can_act = True
            self.timers.append(EventTimer(ENEMY_ACTION * 1000, reset, self))
            

    def set_animation(self, animation):
        if self.active_animation != animation:
            self.active_animation = animation
            self.start_time = pygame.time.get_ticks()

    def handle_animation(self, dt):
        self.anim_frame = int(((pygame.time.get_ticks() - self.start_time) //
                              (1000 / ANIMATION_FRAMERATE)) % len(self.active_animation))
        self.image = self.active_animation[self.anim_frame]
        if self.facing == 'left':
            self.image = pygame.transform.flip(
                self.image, True, False).convert_alpha()
        pass

    def handle_movement(self, dt):
        self.phys_acceleration = self.phys_velocity * -FRICTION_STRENGTH
        self.phys_velocity += self.phys_acceleration * dt
        if self.phys_velocity.magnitude() < 5:
            self.phys_velocity = Vector()

        if self.phys_velocity.magnitude() >= 30 and self.movement_control.dot(self.phys_velocity) < 0:
            self.velocity = self.phys_velocity + self.movement_control - \
                self.movement_control.dot(
                    self.phys_velocity.normalize())*(self.phys_velocity.normalize())
        else:
            self.velocity = self.movement_control + self.phys_velocity
        self.position += self.velocity * dt
        self.rect.centerx = self.position.x

        if self.rect.right < 0:
            self.rect.left = WIN_WIDTH
            self.position = Vector(self.rect.center)
        elif self.rect.left > WIN_WIDTH:
            self.rect.right = 0
            self.position = Vector(self.rect.center)

        for child in self.child_rects:
            child.centerx = self.position.x + child.offset.x

        # Handle x direction collisions
        x_collision = False
        for tile in self.game.layers['tiles']:
            if pygame.Rect.colliderect(tile.rect, self.collision_rect):
                x_collision = True
                if self.phys_velocity.x * self.velocity.x > 0:
                    self.phys_velocity.x = self.phys_velocity.x * .5
                if self.velocity.x > 0:
                    self.rect.right = tile.rect.left + self.rect.right - self.collision_rect.right
                    self.position.x = self.rect.centerx
                elif self.velocity.x < 0:
                    self.rect.left = tile.rect.right + self.rect.left - self.collision_rect.left
                    self.position.x = self.rect.centerx

        self.rect.centery = self.position.y
        for child in self.child_rects:
            child.center = self.position + child.offset

        if self.rect.bottom < 0:
            self.rect.top = WIN_HEIGHT
            self.position = Vector(self.rect.center)
        elif self.rect.top > WIN_HEIGHT:
            self.rect.bottom = 0
            self.position = Vector(self.rect.center)

        y_collision = False
        # Handle y direction collisions
        for tile in self.game.layers['tiles']:
            if pygame.Rect.colliderect(tile.rect, self.collision_rect):
                y_collision = True
                if self.phys_velocity.y * self.velocity.y > 0:
                    self.phys_velocity.y = self.phys_velocity.y * .5
                if self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top + self.rect.bottom - self.collision_rect.bottom
                    self.position.y = self.rect.centery
                elif self.velocity.y < 0:
                    self.rect.top = tile.rect.bottom + self.rect.top - self.collision_rect.top
                    self.position.y = self.rect.centery
        if self.velocity.magnitude() == 0 or (x_collision and self.movement_control.x != 0 and self.movement_control.y == 0) or (y_collision and self.movement_control.y != 0 and self.movement_control.x == 0):
            self.set_animation(self.animations['idle'])
        elif self.movement_control.magnitude() > 10:
            self.set_animation(self.animations['run'])

        for child in self.child_rects:
            child.center = self.position + child.offset

        self.gun.rect.center = self.position + self.gun.rect.offset


    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def attack(self):
        dir = (self.game.player.position - self.position).normalize()
        Bullet(self, self.game.layers['bullets'],
               self.position, dir * BULLET_SPEED)

        # Handle reload
        self.can_attack = False

        def reset(self):
            self.can_attack = True
        self.timers.append(EventTimer(ENEMY_ATTACK * 1000, reset, self))

    def die(self):

        #death animate
        ParticleSpawner(group=self.game.layers['particles'], 
                                position=self.rect.center, 
                                position_radius = 30, 
                                count=20, 
                                color='yellow', 
                                size_range=(10,50), 
                                velocity_range=(200,1500), 
                                acceleration_strength_range=(5,15), 
                                time_range=(.2,1), 
                                angle_range = (0,360))

        self.gun.kill()
        self.kill()

    def update(self, dt):
        self.think(dt)
        self.handle_animation(dt)
        self.handle_movement(dt)
        for timer in self.timers:
            timer.update()
