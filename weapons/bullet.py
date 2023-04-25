from objects.moving_object import MovingObject
import pygame,os,math
from pygame.math import Vector2 as Vector
from game.settings import *
from objects.child_rect import ChildRect
from utils.load_sprites import get_image, get_animation
from objects.particle import ParticleSpawner

class Bullet(MovingObject):
    def __init__(self, group, game, gun, pos, velo, accel = Vector()):
        image = get_image(pygame.image.load(os.path.join('assets', 'misc', 'bullet.png')).convert_alpha(), ANIMATION_TILESIZE, (8,25), 3, (0,2), (12,6)).convert_alpha()
        super().__init__(group, game, image, start_pos=pos, start_velocity=velo, start_acceleration=accel)

        self.gun = gun
        
        # self.image.set_colorkey((0,0,0))
        # self.image = pygame.Surface(BULLET_SIZE)
        # self.image.fill('yellow')
        rotate_angle = math.degrees(math.atan(velo[0]/velo[1]))
        if velo[1] > 0:
            rotate_angle += 180
        self.image = pygame.transform.rotate(self.image, rotate_angle)
        self.rect = self.image.get_rect(center=pos)
        self.collision_mask = pygame.mask.from_surface(self.image)
    
    def on_tile_collide(self, tile):
        self.kill()
    
    def on_enemy_collide(self, enemy):
        enemy.take_damage(10)
        ParticleSpawner(group=self.game.layers['particles'], 
                                position=self.rect.center, 
                                position_radius = 6, 
                                count=5, 
                                color='red', 
                                size_range=(5,10), 
                                velocity_range=(200,300), 
                                acceleration_strength_range=(8,10), 
                                time_range=(.2,1), 
                                angle_range = (0,360))
        self.kill()
    
    def on_player_collide(self):
        self.game.player.take_recoil(self.velocity)
        self.kill()
    
    def is_overlapping(self, object):
        object_mask = pygame.mask.from_surface(object.image)
        overlap = object_mask.overlap_mask(self.collision_mask, (self.rect.centerx - object.rect.centerx, self.rect.centery - object.rect.centery))
        return overlap.count() > 0

    def handle_collision(self):
        self.collision_mask = pygame.mask.from_surface(self.image)
        off_screen = self.rect.right < 0 or self.rect.left > WIN_WIDTH or self.rect.bottom < 0 or self.rect.top > WIN_HEIGHT
        if off_screen:
            self.kill()
        for tile in self.game.layers['tiles']:
            if self.is_overlapping(tile):
                self.on_tile_collide(tile)

        if self.gun.owner is self.game.player:
            for enemy in self.game.layers['enemies']:
                if self.is_overlapping(enemy):
                    self.on_enemy_collide(enemy)
        else:
            if self.is_overlapping(self.game.player):
                self.on_player_collide()



        

    
    def move(self, dt):
        self.velocity += self.phys_acceleration * dt
        self.position += self.velocity * dt
        self.rect.center = self.position
    
    def think(self, dt):
        # Bullets don't think! ;)
        pass