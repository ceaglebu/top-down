import pygame,os,math
from child_rect import ChildRect
from pygame.math import Vector2 as Vector

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

class Gun(pygame.sprite.Sprite):

    def __init__(self, player, group, offset = Vector(0,0)):
        super().__init__(group)
        self.player = player
        self.default_image = pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'shotgun.png')), .5).convert_alpha()
        self.image = pygame.transform.rotate(self.default_image, 0)
        self.offset = offset
        self.rect = ChildRect(self.image.get_rect(), offset)


    def update(self, dt):
        if self.player.mouse_pos[1] != self.player.position.y:
            rotate_angle = math.degrees(math.atan(((abs(self.player.mouse_pos[0] - self.player.position.x)) / (self.player.mouse_pos[1] - self.player.position.y))))
        else:
            rotate_angle = 90
        if self.player.mouse_pos[1] - self.player.position.y < 0:
            rotate_angle += 180
        rotate_angle -= 90
        self.image, self.rect = rot_center(self.default_image, rotate_angle, self.rect.centerx, self.rect.centery)
        if self.player.facing == 'left':
            self.flip = -1
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        else:
            self.flip = 1
        self.rect = ChildRect(self.rect, (self.offset[0] * self.flip, self.offset[1]))
