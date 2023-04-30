import pygame,sys
from pygame.math import lerp
from pygame.math import Vector2 as Vector


class KF_Animation:
    def __init__(self, keyframes):
        self.keyframes = keyframes
        self.keyframes.sort(key= lambda kf: kf.time)
    
    def activate(self):
        self.start_time = pygame.time.get_ticks()
    
    def get_current_frame(self):
        time = pygame.time.get_ticks()
        next_kf_index = 0
        # binary search for what keyframes you are between
        # right now brute forcing it
        for i, kf in enumerate(self.keyframes):
            if kf.time > time - self.start_time:
                next_kf_index = i
                break

        # return lerp between the previous and next for angle and position
        # returns pos, angle
        next_kf = self.keyframes[next_kf_index]
        last_kf = self.keyframes[next_kf_index - 1]
        percentage_between = (time - self.start_time - last_kf.time) / (next_kf.time - last_kf.time) 
        if percentage_between > 1:
            percentage_between = 1
        print(time, self.start_time, last_kf.time, next_kf.time)
        return last_kf.pos.lerp(next_kf.pos, percentage_between), lerp(last_kf.angle, next_kf.angle, percentage_between)

if __name__ == '__main__':     
    from keyframe import Keyframe
    import time,os

    pygame.init()
    
    last = Keyframe(0, (250,0), 0)
    next = Keyframe(2000, (0,200), 10)
    
    animation = KF_Animation([last,next, \
                              Keyframe(2500, (0,0), 0),
                              Keyframe(2750, (200,-200), 0)])
    animation.activate()
    pygame.time.set_timer(pygame.BUTTON_WHEELDOWN, 5000, 1)
    
    clock = pygame.time.Clock()
    run = True

    WIN = pygame.display.set_mode((500,500))
    init_pos = Vector(250,250)
    pos = Vector(init_pos)
    rect = pygame.rect.Rect(init_pos, (0,0)).inflate(50,50)

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.BUTTON_WHEELDOWN:
                run = False

        WIN.fill('black')

        pos = init_pos + animation.get_current_frame()[0]
        rect.center = round(pos)
        pygame.draw.rect(WIN, 'red', rect)
        pygame.display.update()

    pygame.quit()
    sys.exit()
