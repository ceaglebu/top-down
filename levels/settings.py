import pygame

WIN_WIDTH = 1280
WIN_HEIGHT = 720

TILE_SIZE = 64
TILE_ZOOM = 2

GRID_THICKNESS = 2
GRID_COLOR = (50, 50, 50)

GUI_OFFSET = (-50, -50)

PAN_SCROLL_SPEED = 100

TILE_TYPES = [
    ("wall", 'X'),
    ("magnet", 'E'),
    ("infrared", 'H'),
    ("start", 'S') 
]

TILE_COLORS = {
    'X': 'black',
    'E': 'yellow',
    'H': 'red',
    'S': 'green'
}

DIRS = {
    'north': 0,
    'east': 1,
    'south': 2,
    'west': 3
}


