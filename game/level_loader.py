import pygame, os
from utils.load_sprites import get_image
from objects.particle import ParticleGroup
from game.camera import SpriteGroup3d
from game.settings import * 
from pygame.math import Vector2 as Vector
from objects.game_object import GameObject
import random as rand
from objects.enemies import *

COLLIDABLE = ['X']
GROUND = ['O', 'E', 'P']

# Handle changes in level
class LevelLoader():
    def __init__(self, game):
        from assets.environment.tilesets import TILESETS
        self.levels = []
        self.active_level = None
        self.game = game

        self.load(TILESETS['dungeon'], '1')
        self.change_level(0)

    def load(self, tileset, level):
        self.levels.append(Level(os.path.join('levels', f'{level}.txt'), tileset, self.game))
        pass

    def change_level(self, level_index):
        for k, v in self.game.layers.items():
            if isinstance(v, pygame.sprite.Group):
                v.empty()
            elif isinstance(v, ParticleGroup):
                v.particles.clear()
        
        self.active_level = self.levels[level_index]
        self.game.layers['ground'] = self.active_level.ground
        self.game.layers['tiles'] = self.active_level.walls
    
    def spawn_enemies(self):
        self.active_level.spawn_wave()


# Handle loading of itself
class Level():
    def __init__(self, path, tileset, game):
        self.path = path
        self.tileset = tileset
        self.game = game

        self.walls = SpriteGroup3d(self.game.layers['tiles'].z)
        self.ground = SpriteGroup3d(self.game.layers['ground'].z)
        
        self.tile_types = [[]]
        self.tiles = []
        self.spawners = []
        self.load()
    
    def load(self):
        with open(self.path, 'r') as level_file:
            self.tile_types = level_file.readlines()
            for i, row in enumerate(self.tile_types):
                new_row = []
                new_row[:0] = row.strip('\n')
                self.tile_types[i] = new_row
        
        self.tiles = [[0 for _ in range(len(self.tile_types[0]))] for _ in range(len(self.tile_types))]

        for y, row in enumerate(self.tile_types):
            for x, column in enumerate(row):
                if column in COLLIDABLE:

                    mask = [0,1,0,1,1,1,0,1,0]
                    if x != 0 and self.tile_types[y][x-1] in GROUND:
                        mask[3] = 0
                    if x != len(self.tile_types[0]) - 1 and self.tile_types[y][x + 1] in GROUND:
                        mask[5] = 0
                    if y != 0 and self.tile_types[y-1][x] in GROUND:
                        mask[1] = 0
                    if y!= len(self.tile_types) - 1 and self.tile_types[y+1][x] in GROUND:
                        mask[7] = 0

                    self.tiles[y][x] = Tile(self.walls, self.game, (x, y), self.tileset[
                        ','.join(str(m) for m in mask)
                    ])
                elif column in GROUND:
                    mask = [0,0,0,0,0,0,0,0,0]
                    if x != 0 and self.tile_types[y][x-1] in COLLIDABLE:
                        mask[3] = 1
                    if x != len(self.tile_types[0]) - 1 and self.tile_types[y][x + 1] in COLLIDABLE:
                        mask[5] = 1
                    if y != 0 and self.tile_types[y-1][x] in COLLIDABLE:
                        mask[1] = 1
                    if y!= len(self.tile_types) - 1 and self.tile_types[y+1][x] in COLLIDABLE:
                        mask[7] = 1

                    self.tiles[y][x] = Tile(self.ground, self.game, (x, y), self.tileset[
                        ','.join(str(m) for m in mask)
                    ])
                
                if column == 'E':
                    self.spawners.append(Spawner(self.game, self.game.layers['enemies'], (x, y), [(Grunt, 1)]))
        
    def spawn_wave(self):
        for spawner in self.spawners:
            if rand.random() <= spawner.chance:
                spawner.spawn()

# Object being displayed on screen/interacted with by gameobjects
class Tile(GameObject):
    def __init__(self, group, game, coord, image):
        super().__init__(group, game, image, Vector(coord) * TILE_SIZE)
        pass

class Spawner():
    def __init__(self, game, layer, coord, enemy_probability):
        self.chance = .5
        self.game = game
        self.layer = layer
        self.enemy_probability = enemy_probability
        self.coord = coord

    def spawn(self):
        enemy_types = list(map(lambda t: t[0], self.enemy_probability))
        enemy_probabilities = list(map(lambda t: t[1], self.enemy_probability))
        
        enemy = rand.choices(enemy_types, enemy_probabilities, k=1)[0]

        spawnpoint = Vector(self.coord) * TILE_SIZE + Vector(TILE_SIZE,TILE_SIZE) * .5
        new_enemy = enemy(self.layer, self.game, Vector(self.coord) * TILE_SIZE)
