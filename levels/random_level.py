import pygame, os
from pygame.math import Vector2 as Vector
from game.settings import *
from objects.game_object import GameObject
from objects.player import Player
import random as rand
from objects.enemies import *
from levels.level_generator import LevelGenerator

class LevelLoader:
    def __init__(self, game):
        self.game = game
        self.current_chunk = None 
        self.spawners = []
        self.level = {}
    
    def load_random_level(self):
        self.create_level_from_dict(LevelGenerator().generate_level_dict())
    
    def load_level_from_file(self, path):
        pass

    def create_level_from_dict(self, dict):
        from assets.environment.tilesets import TILESETS
        level = {}
        for coord, tile_type in dict.items():
            x, y = (int(x) for x in coord.split(','))
            chunk = None
            chunk_coord = (x // CHUNK_SIZE, y // CHUNK_SIZE)
            chunk_string = ','.join(str(e) for e in chunk_coord)
            if chunk_string in level:
                chunk = level[chunk_string]
            else:
                chunk = level[chunk_string] = Chunk()

            group = None
            image = None
            if tile_type in COLLIDABLE:

                group = chunk.walls
                
                # Get proper image
                mask = [0,1,0,1,1,1,0,1,0]
                if x != 0 and f'{x - 1},{y}' in dict and dict[f'{x - 1},{y}'] in GROUND:
                    mask[3] = 0
                if f'{x + 1},{y}' in dict and dict[f'{x + 1},{y}'] in GROUND:
                    mask[5] = 0
                if y != 0 and f'{x},{y-1}' in dict and dict[f'{x},{y-1}'] in GROUND:
                    mask[1] = 0
                if f'{x},{y + 1}' in dict and dict[f'{x},{y + 1}'] in GROUND:
                    mask[7] = 0
                image = TILESETS['dungeon'][','.join(str(m) for m in mask)] 

            elif tile_type in GROUND:
                group = chunk.ground

                mask = [0,0,0,0,0,0,0,0,0]
                if x != 0 and f'{x-1},{y}' in dict and dict[f'{x-1},{y}'] in COLLIDABLE:
                    mask[3] = 1
                if f'{x + 1},{y}' in dict and dict[f'{x+1},{y}'] in COLLIDABLE:
                    mask[5] = 1
                if y != 0 and f'{x},{y-1}' in dict and dict[f'{x},{y-1}'] in COLLIDABLE:
                    mask[1] = 1
                if f'{x},{y + 1}' in dict and dict[f'{x},{y+1}'] in COLLIDABLE:
                    mask[7] = 1

                image = TILESETS['dungeon'][','.join(str(m) for m in mask)]
            
            group.append(Tile(None, self.game, (x, y), image))

            if tile_type == 'P':
                self.game.player = Player(self.game.layers['player'], self.game, Vector((x, y)) * TILE_SIZE)
            elif tile_type == 'E':
                print('spawner')
                chunk.spawners.append(Spawner(self.game, self.game.layers['enemies'], chunk, (x,y), [(Grunt, 1)]))
        self.level = level
        self.handle_chunk_update()   

    def new_chunks(self, player_chunk):
        self.game.layers['ground'].empty()
        self.game.layers['tiles'].empty()
        self.game.layers['enemies'].empty()
        self.game.layers['accessories'].empty()
        self.game.layers['accessories'].add_internal(self.game.player.gun)
        self.spawners = []

        self.current_chunk = player_chunk
        loaded_chunks = []
        for x in range(CHUNKS_LOADED[0]):
            for y in range(CHUNKS_LOADED[1]):
                loaded_chunks.append((player_chunk[0] - CHUNKS_LOADED[0] // 2 + x, player_chunk[1] - CHUNKS_LOADED[1] // 2 + y))
        
        for current_chunk in loaded_chunks:
            chunk = None
            chunk_string = ','.join(str(e) for e in current_chunk)
            if chunk_string in self.level:
                chunk = self.level[chunk_string]
            else:
                chunk = self.level[chunk_string] = Chunk()
            chunk.load(self)

    def spawn_enemies(self):
        for spawner in self.spawners:
            spawner.spawn()
            print(spawner.coord)
    
    def handle_chunk_update(self):
        player_chunk = [int(x) for x in Vector(self.game.player.position) / TILE_SIZE / CHUNK_SIZE]
        if player_chunk != self.current_chunk:
            self.new_chunks(player_chunk)
    
    def update(self, dt):
        self.handle_chunk_update()

class Chunk:
    def __init__(self):
        self.walls = []
        self.ground = []
        self.enemies = []
        self.spawners = []
    
    def load(self, level_loader):
        for tile in self.walls:
            level_loader.game.layers['tiles'].add_internal(tile)
        
        for ground in self.ground:
            level_loader.game.layers['ground'].add_internal(ground)
        
        for enemy in self.enemies:
            dead_enemies = []
            if enemy.is_alive:
                level_loader.game.layers['enemies'].add_internal(enemy)
                level_loader.game.layers['accessories'].add_internal(enemy.gun)
            else:
                dead_enemies.append(enemy)

            for enemy in dead_enemies:
                self.enemies.remove(enemy)
        
        for spawner in self.spawners:
            level_loader.spawners.append(spawner)


class Tile(GameObject):
    def __init__(self, group, game, coord, image):
        super().__init__(group, game, image, Vector(coord) * TILE_SIZE)

class Spawner():
    def __init__(self, game, layer, chunk, coord, enemy_probability):
        self.chance = 1
        self.game = game
        self.layer = layer
        self.chunk = chunk
        self.enemy_probability = enemy_probability
        self.coord = coord

    def spawn(self):
        enemy_types = list(map(lambda t: t[0], self.enemy_probability))
        enemy_probabilities = list(map(lambda t: t[1], self.enemy_probability))
        
        enemy = rand.choices(enemy_types, enemy_probabilities, k=1)[0]
        new_enemy = enemy(self.layer, self.game, Vector(self.coord) * TILE_SIZE)
        self.chunk.enemies.append(new_enemy)