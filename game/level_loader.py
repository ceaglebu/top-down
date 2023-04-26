import pygame, os
from utils.load_sprites import get_image
from objects.particle import ParticleGroup
from game.camera import SpriteGroup3d
from game.settings import * 
from pygame.math import Vector2 as Vector
from objects.game_object import GameObject

# Handle changes in level
class LevelLoader():
    def __init__(self, game):
        from assets.environment.tilesets import TILESETS
        self.levels = []
        self.game = game

        self.load(TILESETS['dungeon'])
        self.change_level(0)

    def load(self, tileset):
        self.levels.append(Level(os.path.join('levels', 'test.txt'), tileset, self.game))
        pass

    def change_level(self, level_index):
        for k, v in self.game.layers.items():
            if isinstance(v, pygame.sprite.Group):
                v.empty()
            elif isinstance(v, ParticleGroup):
                v.particles.clear()
        
        self.game.layers['ground'] = self.levels[level_index].ground
        self.game.layers['tiles'] = self.levels[level_index].walls
        
    



# Handle loading of itself
class Level():
    def __init__(self, path, tileset, game):
        self.path = path
        self.tileset = tileset
        self.game = game

        self.walls = SpriteGroup3d(self.game.layers['tiles'].z)
        self.ground = SpriteGroup3d(self.game.layers['ground'].z)
        
        self.tile_types = [[]]
        self.tiles = [
            []
        ]
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
                mask = '0,0,0,0,0,0,0,0,0'
                if column == 'X':
                    print("ground")
                    self.tiles[y][x] = 1
                    Tile(self.walls, self.game, (x, y), self.tileset[
                        '0,0,0,0,1,0,0,0,0'
                    ])
                else:
                    Tile(self.ground, self.game, (x, y), self.tileset[
                        '0,0,0,0,0,0,0,0,0'
                    ])

# Object being displayed on screen/interacted with by gameobjects
class Tile(GameObject):
    def __init__(self, group, game, coord, image):
        super().__init__(group, game, image, Vector(coord) * TILE_SIZE)
        pass

