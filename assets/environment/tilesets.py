import os
import pygame
from utils.load_sprites import get_image
from game.settings import TILE_SIZE

SPRITESHEETS = {
    'dungeon-floor': pygame.image.load(os.path.join('assets', 'environment', 'dungeon-floor.png')),
    'dungeon-wall': pygame.image.load(os.path.join('assets', 'environment', 'dungeon-wall.png'))
}

TILESETS = {
    'dungeon': {
        # Each key is a 2d array representing the tile and its 8 neighbors
        # 1 = wall,0 = ground
        
        # Floor tiles

        #0 Surrounding walls
        '0,0,0,0,0,0,0,0,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (1,0)),

        # 1 surrounding wall
        '0,1,0,0,0,0,0,0,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (2,0)),
        '0,0,0,0,0,1,0,0,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (0,1)),
        '0,0,0,0,0,0,0,1,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (4,1)),
        '0,0,0,1,0,0,0,0,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (3,0)),
        
        # 2 surrounding walls
        '0,1,0,0,0,1,0,0,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (1,1)),
        '0,1,0,0,0,0,0,1,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (0,2)),
        '0,1,0,1,0,0,0,0,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (4,0)),
        '0,0,0,0,0,1,0,1,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (3,2)),
        '0,0,0,1,0,1,0,0,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (2,1)),
        '0,0,0,1,0,0,0,1,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (1,2)),

        # 3 surrounding walls
        '0,1,0,0,0,1,0,1,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (4,2)),
        '0,1,0,1,0,1,0,0,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (3,1)),
        '0,1,0,1,0,0,0,1,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (2,2)),
        '0,0,0,1,0,1,0,1,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (0,3)),

        # 4 surrounding walls
        '0,1,0,1,0,1,0,1,0':  get_image(SPRITESHEETS['dungeon-floor'], (32,32), (32,32), TILE_SIZE/32, (1,3)),

        # Wall tiles
        #0 = floor,1 = wall

        # No corner shenanigans
        #0 surrounding ground
        '0,1,0,1,1,1,0,1,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (6,5)),
        
        #1 surrounding ground
        '0,0,0,1,1,1,0,1,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (2,5)),
        '0,1,0,1,1,0,0,1,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (4,3)),
        '0,1,0,1,1,1,0,0,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (4,1)),
        '0,1,0,0,1,1,0,0,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (4,4)),
        
        # 2 surrounding ground
        '0,0,0,1,1,0,0,1,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (2,3)),
        '0,0,0,1,1,1,0,0,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (0,1)),
        '0,0,0,0,1,1,0,1,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (2,4)),
        '0,1,0,1,1,0,0,0,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (4,0)),
        '0,1,0,0,1,0,0,1,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (6,1)),
        '0,1,0,0,1,1,0,0,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (7,0)),
        
        # 3 surrounding ground
        '0,0,0,1,1,0,0,0,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (2,0)),
        '0,0,0,0,1,0,0,1,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (5,1)),
        '0,0,0,0,1,1,0,0,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (5,0)),
        '0,1,0,0,1,0,0,0,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (1,0)),
        
        # 4 surrounding ground
        '0,0,0,0,1,0,0,0,0':  get_image(SPRITESHEETS['dungeon-wall'], (32,32), (32,32), TILE_SIZE/32, (7,5)),
        
        # Corner shenanigans
        
        # for another time this shit is confusing bruh, might have to refactor to do it );

    }
}