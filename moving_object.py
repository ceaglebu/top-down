import pygame,sys,os
from pygame.math import Vector2 as Vector
from settings import *
from event_timer import EventTimer, Timer
from load_sprites import get_animation
from child_rect import ChildRect
from bullet import Bullet
from gun import Gun
from particle import *

class MovingObject(pygame.sprite.Sprite):

    def __init__(self, group, game, animations, active_animation, start_pos=Vector(WIN_WIDTH / 2, WIN_HEIGHT / 2)):
        # Initialize
        super().__init__(group)
        self.game = game
        self.screen = pygame.display.get_surface()
        self.child_rects = []
        self.child_sprites = pygame.sprite.Group()

        # Movement vectors
        self.position = start_pos
        self.velocity = Vector()
        self.phys_velocity = Vector() # Physics are independent of player movement
        self.phys_acceleration = Vector()

        # Animation
        self.start_time = pygame.time.get_ticks()
        self.animations = animations
        self.active_animation = active_animation
        self.anim_frame = 0
        self.facing = 'right'
        self.image = self.active_animation[self.anim_frame]
        self.rect = self.image.get_rect()
        self.rect.center = ((0, 0))

        # Sprite
        self.collision_rect = ChildRect(pygame.Rect(self.rect.center, (0,0)).inflate(Vector(self.rect.size)* COLLISION_FORGIVENESS), (0, int(self.rect.height - COLLISION_FORGIVENESS * self.rect.height) / 2))
        self.child_rects.append(self.collision_rect)

        self.timers = []
        self.movement_control = Vector()


    def think(self, dt):
        pass

    
    def set_animation(self, animation):
        if self.active_animation != animation:
            self.active_animation = animation
            self.start_time = pygame.time.get_ticks()

    def handle_animation(self, dt):
        self.anim_frame = int(((pygame.time.get_ticks() - self.start_time) // (1000 / ANIMATION_FRAMERATE)) % len(self.active_animation))
        self.image = self.active_animation[self.anim_frame]
        if self.facing == 'left':
            self.image = pygame.transform.flip(self.image, True, False).convert_alpha()
        pass
        
    def move(self, dt):
        self.phys_acceleration = self.phys_velocity * -FRICTION_STRENGTH
        self.phys_velocity += self.phys_acceleration * dt
        if self.phys_velocity.magnitude() < 5:
            self.phys_velocity = Vector()

        if self.phys_velocity.magnitude() >= 30 and self.movement_control.dot(self.phys_velocity) < 0:
            self.velocity = self.phys_velocity + self.movement_control - self.movement_control.dot(self.phys_velocity.normalize())*(self.phys_velocity.normalize())
        else:
            self.velocity = self.movement_control + self.phys_velocity 
        self.position += self.velocity * dt

        x_collide = self.handle_x_collision()
        y_collide = self.handle_y_collision()
        return (x_collide, y_collide)


    def handle_x_collision(self):
        # Update position to check for collision
        self.rect.centerx = self.position.x
        for child in self.child_rects:
            child.centerx = self.position.x + child.offset.x

        # Check for window border collisions
        if self.rect.right < 0:
            self.rect.left = WIN_WIDTH
            self.position = Vector(self.rect.center)
        elif self.rect.left > WIN_WIDTH:
            self.rect.right = 0
            self.position = Vector(self.rect.center)

        # Check for object collisions
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
        
        # Move child back if it collided
        for child in self.child_rects:
            child.centerx = self.position.x + child.offset.x

        return x_collision

    def handle_y_collision(self):
        self.rect.centery = self.position.y
        for child in self.child_rects:
            child.centery = self.position.y + child.offset.y

        if self.rect.bottom < 0:
            self.rect.top = WIN_HEIGHT
            self.position = Vector(self.rect.center)
        elif self.rect.top > WIN_HEIGHT:
            self.rect.bottom = 0
            self.position = Vector(self.rect.center)

        y_collision = False
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

        for child in self.child_rects:
            child.centery = self.position.y + child.offset.y

        return y_collision
    
    def post_collision(self, dt, collide):
        pass


    def update(self, dt):
        self.think(dt)
        self.handle_animation()
        collide = self.move(dt)

        self.post_collision(dt, collide)

        for timer in self.timers:
            timer.update()
