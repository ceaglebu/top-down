import pygame,math
import random as rand
from pygame.math import Vector2 as Vector

class ParticleSpawner():
    def __init__(self, group, position, position_radius, count, color, size_range, velocity_range, acceleration_strength_range, time_range, angle_range):
        for _ in range(count):
            pos = (position[0] + rand.randint(-position_radius, position_radius), position[1] + rand.randint(-position_radius, position_radius))
            angle = rand.uniform(angle_range[0], angle_range[1])
            unit_vector = Vector(math.cos(math.radians(angle)), -math.sin(math.radians(angle)))
            size = rand.randint(size_range[0], size_range[1])
            #velo = ((rand.random() ** 1/2) * (velocity_range[1] - velocity_range[0]) + velocity_range[0]) * unit_vector
            velo = rand.uniform(velocity_range[0], velocity_range[1]) * unit_vector
            accel_strength = rand.uniform(acceleration_strength_range[0], acceleration_strength_range[1])
            shrinkspeed = size / rand.uniform(time_range[0], time_range[1])

            group.particles.append(Particle(color, pos, size, velo, accel_strength, shrinkspeed))

class ParticleGroup():
    def __init__(self):
        self.particles = []

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)

    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, particle.color, particle.position, particle.size / 2)

class Particle():
    def __init__(self, color, position, size, velocity, accel_strength, shrinkspeed):
        self.color = color
        self.size = size
        self.position = Vector(position)
        self.velocity = Vector(velocity)
        self.accel_strength = accel_strength
        self.shrinkspeed = shrinkspeed
    
    def update(self, dt):
        self.velocity -= self.velocity * self.accel_strength * dt
        self.position += self.velocity * dt
        self.size -= self.shrinkspeed * dt

if __name__ == '__main__':
    pygame.init()

    win = pygame.display.set_mode((1280,720))

    group = ParticleGroup()
    particles = ParticleSpawner(group = group, 
                                position=(win.get_width() //2, win.get_height() // 2), 
                                position_radius=10, 
                                count=20, 
                                color='red', 
                                size_range=(10,20), 
                                velocity_range=(0, 1500), 
                                acceleration_strength_range=(10,15), 
                                time_range=(1,1), 
                                angle_range=(0,360))
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000
        print(1/dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        win.fill((50,50,50))
        group.update(dt)
        group.draw(win)
        pygame.display.update()