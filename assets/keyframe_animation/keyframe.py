from pygame.math import Vector2 as Vector

class Keyframe:
    def __init__(self, time, pos, angle):
        self.time = time
        self.pos = Vector(pos)
        self.angle = angle