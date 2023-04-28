import pygame

WIN_WIDTH = 1260
WIN_HEIGHT = 720
BACKGROUND_COLOR = (28,17,23)
TILE_SIZE = 50

ANIMATION_FRAMERATE = 6
ANIMATION_TILESIZE = (32,32)

PLAYER_SPEED = 400
PLAYER_SCALE = 3.5
COLLISION_FORGIVENESS = .8

ENEMY_SPEED = 400
ENEMY_ATTACK = .4
ENEMY_ACTION = .2

ROLL_COOLDOWN = 500
ROLL_STRENGTH = 1500
ROLL_PARTICLE_COOLDOWN = 100

FRICTION_STRENGTH = 10
RECOIL_STRENGTH = 0
PLAYER_KNOCKBACK_STRENGTH = 700

BULLET_SIZE = (100,50)
RELOAD_TIME = .2
ENABLE_SPRAY = True

BULLET_SPEED = {
    'player': 1500,
    'enemy': 500
}

CAMERA_SHAKE_INTENSITY = 200
ENEMY_DIES_SHAKE_INTENSITY = 1000
SHOOTING_SHAKE_INTENSITY = 200

BULLET_TIME_FACTOR = .15

EVENTS = {
    'player_roll': pygame.USEREVENT + 1
}