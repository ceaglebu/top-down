import math
from abilities.ability import Ability
from utils.math import snorm
from objects.particle import ParticleSpawner
from game.event_timer import EventTimer


class Reflect(Ability):
    def __init__(self, game, player, cooldown=5000, dist_threshold=500):
        super().__init__(game, player, cooldown)
        self.dist_threshold = dist_threshold

    def pop(self):
        player = self.player
        p_center = player.rect.center

        ParticleSpawner(group=self.game.layers['particles'],
                            position=p_center,
                            position_radius=0,
                            count=20,
                            color='cyan',
                            size_range=(10, 20),
                            velocity_range=(1500, 1500),
                            acceleration_strength_range=(10, 10),
                            time_range=(.2, 1),
                            angle_range=(0, 360))

        self.game.start_bullet_time(length = 100)
        self.game.timers.append(EventTimer(100, self.reflect))
    
    def reflect(self):
        for bullet in self.game.layers['bullets']:
            if bullet.gun.owner is not self.player:
                b_center = bullet.rect.center
                dist = math.dist(b_center, self.player.rect.center)
                if dist <= self.dist_threshold:
                    bullet.gun = self.player.gun
                    bullet.velocity = snorm(
                        bullet.position - self.player.position, bullet.gun.speed)