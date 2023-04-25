import pygame

class AnimationData():
    def __init__(self, animation_map, active_animation):
        self.start_time = pygame.time.get_ticks()
        self.animations = animation_map
        self.active_animation = active_animation
        self.frame = 0