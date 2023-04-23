import pygame

class ChildRect(pygame.Rect):
    def __init__(self, rect, offset = (0,0)):
        super().__init__(rect)
        self.offset = pygame.math.Vector2((int(offset[0]), int(offset[1])))
        self.default_offset = pygame.math.Vector2((int(offset[0]), int(offset[1])))