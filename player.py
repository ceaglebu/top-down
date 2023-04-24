import pygame,sys,os
from pygame.math import Vector2 as Vector
from settings import *
from event_timer import EventTimer, Timer
from load_sprites import get_animation
from child_rect import ChildRect
from bullet import Bullet
from gun import Gun
from particle import *

class Player(pygame.sprite.Sprite):

    def __init__(self, group, game):
        # Initialize
        super().__init__(group)
        self.game = game
        self.screen = pygame.display.get_surface()
        self.child_rects = []
        self.child_sprites = pygame.sprite.Group()

        # Movement vectors
        self.position = Vector(WIN_WIDTH / 2, WIN_HEIGHT / 2)
        self.velocity = Vector()
        self.phys_velocity = Vector() # Physics are independent of player movement
        self.phys_acceleration = Vector()

        # Animation
        self.start_time = pygame.time.get_ticks()
        sprite_sheet = pygame.image.load(os.path.join('assets', 'player', 'mPlayer_ [human].png')).convert_alpha()
        self.animations = {
            'idle': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11,16), PLAYER_SCALE, 1, 0, 4, (11,12)),
            'roll': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11,16), PLAYER_SCALE, 6, 3, 5, (11,12)),
            'run': get_animation(sprite_sheet, ANIMATION_TILESIZE, (11,16), PLAYER_SCALE, 2, 0, 8, (11,12))
        }
        self.active_animation = self.animations['idle']
        self.anim_frame = 0
        self.facing = 'right'
        self.image = self.active_animation[self.anim_frame]
        self.rect = self.image.get_rect()
        self.rect.center = ((0, 0))

        # Particles

        self.roll_particle_spawner = ParticleSpawner(group=self.game.layers['player-particles'], 
                                position=(0,0), 
                                position_radius = 5, 
                                count=3, 
                                color=((10,10,10)), 
                                size_range=(10,20), 
                                velocity_range=(50,100), 
                                acceleration_strength_range=(5,7), 
                                time_range=(.2,1), 
                                angle_range = (150,390),
                                recallable=True)

        # Sprite
        self.collision_rect = ChildRect(pygame.Rect(self.rect.center, (0,0)).inflate(Vector(self.rect.size)* COLLISION_FORGIVENESS), (0, int(self.rect.height - COLLISION_FORGIVENESS * self.rect.height) / 2))
        self.child_rects.append(self.collision_rect)

        self.gun = Gun(self, self.game.layers['accessories'],(20,20))

        # State
        self.is_rolling = False
        self.can_roll = True
        self.reload = True

    def handle_controls(self, dt):
        self.keys_down = pygame.key.get_pressed()
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        if self.mouse_pos[0] > self.rect.centerx:
            self.facing = 'right'
        else:
            self.facing = 'left'

        self.movement_control = Vector()

        if self.keys_down[pygame.K_w] or self.keys_down[pygame.K_UP]:
            self.movement_control.y = -1
        elif self.keys_down[pygame.K_s] or self.keys_down[pygame.K_DOWN]:
            self.movement_control.y = 1
        else:
            self.movement_control.y = 0

        if self.keys_down[pygame.K_d] or self.keys_down[pygame.K_RIGHT]:
            self.movement_control.x = 1
        elif self.keys_down[pygame.K_a] or self.keys_down[pygame.K_LEFT]:
            self.movement_control.x = -1
        else:
            self.movement_control.x = 0

        if self.movement_control.magnitude() != 0:
            self.movement_control = self.movement_control.normalize() * PLAYER_SPEED

        if self.keys_down[pygame.K_SPACE] and self.can_roll and self.phys_velocity.magnitude() <= 500 and self.movement_control.magnitude() != 0:
            self.is_rolling = True
            self.can_roll = False
            self.collision_rect.height *= 3 / 4
            self.collision_rect.offset.y = int((self.rect.bottom - self.collision_rect.bottom) * COLLISION_FORGIVENESS)
            self.set_animation(self.animations['roll'])
            self.start_roll_particles()
            
            def reset_roll(self):
                self.can_roll = True
            self.game.timers.append(EventTimer(ROLL_COOLDOWN * 1000, reset_roll, self))

            def end_roll(self):
                self.is_rolling = False
                self.collision_rect.height = self.rect.height * COLLISION_FORGIVENESS
                self.collision_rect.offset.y = self.collision_rect.default_offset.y
                if self.active_animation == self.animations['roll']:
                    self.set_animation(self.animations['idle'])
            self.game.timers.append(EventTimer(3 * 1000 / FRICTION_STRENGTH, end_roll, self))

            if self.movement_control.magnitude() != 0:
                self.phys_velocity += self.movement_control.normalize() * ROLL_STRENGTH
        
        click = False
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
            
        if (click or (self.mouse_buttons[0] and ENABLE_SPRAY)) and self.reload: 
            # Create bullet
            dir = (self.mouse_pos - self.position).normalize()
            Bullet(self, self.game.layers['bullets'], self.gun.get_endpoint(), dir * BULLET_SPEED)
            ParticleSpawner(group=self.game.layers['particles'], 
                                position=self.gun.get_endpoint(), 
                                position_radius = 5, 
                                count=3, 
                                color='yellow', 
                                size_range=(1, 10), 
                                velocity_range=(200,1500), 
                                acceleration_strength_range=(5,15), 
                                time_range=(.2,1), 
                                angle_range = (self.gun.angle -30, self.gun.angle + 30))

            # Handle recoil
            self.phys_velocity += RECOIL_STRENGTH * (self.position - self.mouse_pos).normalize()

            # Handle reload
            self.reload = False
            def reload(self):
                self.reload = True
            self.game.timers.append(EventTimer(RELOAD_TIME * 1000, reload, self))
        elif click and not self.reload:
            # play clicking sound effect
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
        
    def start_roll_particles(self):
        def spawn_roll_particles(self):
            if self.is_rolling:
                self.roll_particle_spawner.spawn(4, self.collision_rect.midbottom)
                self.game.timers.append(EventTimer(ROLL_PARTICLE_COOLDOWN * 1000, spawn_roll_particles, self))
        spawn_roll_particles(self)                
        self.game.timers.append(EventTimer(ROLL_PARTICLE_COOLDOWN * 1000, spawn_roll_particles, self))
        
        pass

    def handle_movement(self, dt):
        self.phys_acceleration = self.phys_velocity * -FRICTION_STRENGTH
        self.phys_velocity += self.phys_acceleration * dt
        if self.phys_velocity.magnitude() < 5:
            self.phys_velocity = Vector()

        if self.phys_velocity.magnitude() >= 30 and self.movement_control.dot(self.phys_velocity) < 0:
            self.velocity = self.phys_velocity + self.movement_control - self.movement_control.dot(self.phys_velocity.normalize())*(self.phys_velocity.normalize())
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
        if self.velocity.magnitude() == 0 or (not self.is_rolling and ((x_collision and self.movement_control.x != 0 and self.movement_control.y == 0) or (y_collision and self.movement_control.y != 0 and self.movement_control.x == 0))):
            self.set_animation(self.animations['idle'])
        elif not self.is_rolling and self.movement_control.magnitude() > 10:
            self.set_animation(self.animations['run'])
        
        for child in self.child_rects:
            child.center = self.position + child.offset
        
        self.gun.rect.center = self.position + self.gun.rect.offset


    def update(self, dt):
        self.handle_controls(dt)
        self.handle_animation(dt)
        self.handle_movement(dt)
