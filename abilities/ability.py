import math
from game.event_timer import EventTimer
from game.settings import FRICTION_STRENGTH, ROLL_COOLDOWN, ROLL_PARTICLE_COOLDOWN, ROLL_STRENGTH
from objects.particle import ParticleSpawner
from pygame.math import Vector2 as Vector
from utils.math import snorm
import pygame


class Ability:
    def __init__(self, game, cooldown, key=pygame.K_e, duration=0):
        self.game = game
        self.cooldown = cooldown
        self.can_use = True
        self.is_active = False
        self.key = key
        self.duration = duration

    def reset_can_use(self):
        self.can_use = True
    
    def on_ability_end(self):
        self.is_active = False

    def can_pop(self):
        return self.can_use

    def use(self):
        if self.can_pop():
            if self.cooldown != 0:
                self.can_use = False
                self.game.timers.append(EventTimer(
                    self.cooldown, self.reset_can_use))
            if self.duration != 0:
                self.is_active = True
                self.game.timers.append(EventTimer(self.duration, self.on_ability_end))
            self.pop()
        else:
            # play failed ability sound?
            pass

    def pop(self):
        pass


class ReflectAbility(Ability):
    def __init__(self, game, cooldown=5000, dist_threshold=500):
        super().__init__(game, cooldown)
        self.dist_threshold = dist_threshold

    def pop(self):
        player = self.game.player
        p_center = player.rect.center
        for bullet in self.game.layers['bullets']:
            if bullet.gun.owner is not player:
                b_center = bullet.rect.center
                dist = math.dist(b_center, p_center)
                if dist <= self.dist_threshold:
                    bullet.gun = player.gun
                    bullet.velocity = snorm(
                        bullet.position - player.position, bullet.gun.speed)


class Roll(Ability):
    def __init__(self, game, player, cooldown=(ROLL_COOLDOWN), key=pygame.K_SPACE, particle_cooldown=(ROLL_PARTICLE_COOLDOWN)):
        super().__init__(game, cooldown, key, duration=(3000/FRICTION_STRENGTH))
        self.particle_cooldown = particle_cooldown
        self.player = player
        self.roll_particle_spawner = ParticleSpawner(group=self.game.layers['player-particles'],
                                                     position=(0, 0),
                                                     position_radius=5,
                                                     count=3,
                                                     color=((10, 10, 10)),
                                                     size_range=(10, 20),
                                                     velocity_range=(50, 100),
                                                     acceleration_strength_range=(
                                                         5, 7),
                                                     time_range=(.2, 1),
                                                     angle_range=(150, 390),
                                                     recallable=True)

    def pop(self):
        self.start_roll()

    def can_pop(self):
        return self.can_use and self.player.phys_velocity.magnitude(
        ) <= 500 and self.player.movement_control.magnitude() != 0

    def on_ability_end(self):
            super().on_ability_end()
            self.player.set_animation('idle')

    def spawn_roll_particles(self):
        if self.is_active:
            self.roll_particle_spawner.spawn(
                4, self.player.collision_rect.midbottom)
            self.game.timers.append(EventTimer(
                self.particle_cooldown, self.spawn_roll_particles))

    def start_roll(self):
        self.player.set_animation('roll')
        self.spawn_roll_particles()

        if self.player.movement_control.magnitude() != 0:
            self.player.phys_velocity += self.player.movement_control.normalize() * \
                ROLL_STRENGTH
