import pygame,math
import random as rand
from pygame.math import Vector2 as Vector

class ParticleSpawner():
    def __init__(self, group, position, position_radius, count, color, size_range, velocity_range, acceleration_strength_range, time_range, angle_range, recallable=False):

        if not recallable:
            for _ in range(count):
                pos = (position[0] + rand.randint(-position_radius, position_radius), position[1] + rand.randint(-position_radius, position_radius))
                angle = rand.uniform(angle_range[0], angle_range[1])
                unit_vector = Vector(math.cos(math.radians(angle)), -math.sin(math.radians(angle)))
                size = rand.randint(size_range[0], size_range[1])
                velo = rand.uniform(velocity_range[0], velocity_range[1]) * unit_vector
                accel_strength = rand.uniform(acceleration_strength_range[0], acceleration_strength_range[1])
                shrinkspeed = size / rand.uniform(time_range[0], time_range[1])

                group.particles.append(Particle(color, pos, size, velo, accel_strength, shrinkspeed))
        else:
            self.group = group
            self.position = position
            self.position_radius = position_radius
            self.color = color
            self.size_range = size_range
            self.velocity_range = velocity_range
            self.acceleration_strength_range = acceleration_strength_range
            self.time_range = time_range
            self.angle_range = angle_range
    
    def spawn(self, count, spawn_pos = None):
        if spawn_pos == None:
            spawn_pos = self.position
        else: 
            self.position = spawn_pos
        
        for _ in range(count):
            pos = (self.position[0] + rand.randint(-self.position_radius, self.position_radius), self.position[1] + rand.randint(-self.position_radius, self.position_radius))
            angle = rand.uniform(self.angle_range[0], self.angle_range[1])
            unit_vector = Vector(math.cos(math.radians(angle)), -math.sin(math.radians(angle)))
            size = rand.randint(self.size_range[0], self.size_range[1])
            velo = rand.uniform(self.velocity_range[0], self.velocity_range[1]) * unit_vector
            accel_strength = rand.uniform(self.acceleration_strength_range[0], self.acceleration_strength_range[1])
            shrinkspeed = size / rand.uniform(self.time_range[0], self.time_range[1])

            self.group.particles.append(Particle(self.color, pos, size, velo, accel_strength, shrinkspeed))

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