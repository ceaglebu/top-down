from abilities.ability import Ability
from game.event_timer import EventTimer
from game.settings import FRICTION_STRENGTH, ROLL_COOLDOWN, ROLL_PARTICLE_COOLDOWN, ROLL_STRENGTH
from objects.particle import ParticleSpawner
import pygame

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