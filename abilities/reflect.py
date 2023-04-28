import math
from abilities.ability import Ability
from utils.math import snorm


class Reflect(Ability):
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