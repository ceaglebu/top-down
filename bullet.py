import pygame,os,math
from pygame.math import Vector2 as Vector
from settings import *
from child_rect import ChildRect
from load_sprites import get_image, get_animation
from particle import ParticleSpawner

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, group, pos, velo, accel = Vector()):
        super().__init__(group)
        self.player = player
        
        self.image = get_image(pygame.image.load(os.path.join('assets', 'misc', 'bullet.png')).convert_alpha(), ANIMATION_TILESIZE, (8,25), 3, (0,2), (12,6)).convert_alpha()
        # self.image.set_colorkey((0,0,0))
        # self.image = pygame.Surface(BULLET_SIZE)
        # self.image.fill('yellow')
        rotate_angle = math.degrees(math.atan(velo[0]/velo[1]))
        if velo[1] > 0:
            rotate_angle += 180
        self.image = pygame.transform.rotate(self.image, rotate_angle)
        self.rect = self.image.get_rect(center=pos)
        self.collision_mask = pygame.mask.from_surface(self.image)

        self.position = Vector(pos)
        self.velo = Vector(velo)
        self.accel = Vector(accel)

    def update(self, dt):
        self.velo += self.accel * dt
        self.position += self.velo * dt
        self.rect.center = self.position
        self.collision_mask = pygame.mask.from_surface(self.image)
        if self.rect.right < 0 or self.rect.left > WIN_WIDTH or self.rect.bottom < 0 or self.rect.top > WIN_HEIGHT:
            self.kill()
        for tile in self.player.game.layers['tiles']:
            tile_mask = pygame.mask.from_surface(tile.image)
            overlap = tile_mask.overlap_mask(self.collision_mask, (self.rect.centerx - tile.rect.centerx, self.rect.centery - tile.rect.centery))
            if overlap.count() > 0:
                self.kill()
        for enemy in self.player.game.layers['enemies']:
            tile_mask = pygame.mask.from_surface(tile.image)
            overlap = tile_mask.overlap_mask(self.collision_mask, (self.rect.centerx - enemy.rect.centerx, self.rect.centery - enemy.rect.centery))
            if overlap.count() > 0:
                enemy.take_damage(10)
                ParticleSpawner(group=self.player.game.layers['particles'], 
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