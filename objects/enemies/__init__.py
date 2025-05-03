from objects.enemies.enemy import Enemy
from objects.enemies.grunt import Grunt
from objects.enemies.sniper import Sniper

enemy_types = {
    'easy': [Grunt],
    'medium': [Grunt, Sniper]
}