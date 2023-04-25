import pygame
from pygame.math import Vector2 as Vector

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

def snorm(vector, speed):
    if (vector.magnitude() == 0):
        return Vector()
    else:
        return vector.normalize() * speed