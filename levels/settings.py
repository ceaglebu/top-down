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
    ("ground", 'O'),
    ("spawner", 'E'),
    ("player", 'P'),
]

TILE_COLORS = {
    'X': 'black',
    'O': 'white',
    'E': 'red',
    'P': 'green',
}


