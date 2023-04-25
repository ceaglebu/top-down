import pygame

WIN_WIDTH = 1260
WIN_HEIGHT = 720
ANIMATION_FRAMERATE = 6
ANIMATION_TILESIZE = (32,32)

PLAYER_SPEED = 400
PLAYER_SCALE = 4
COLLISION_FORGIVENESS = .8

ENEMY_SPEED = 400
ENEMY_ATTACK = 4
ENEMY_ACTION = 1

ROLL_COOLDOWN = .5
ROLL_STRENGTH = 1500
ROLL_PARTICLE_COOLDOWN = .1

FRICTION_STRENGTH = 10
RECOIL_STRENGTH = 250
PLAYER_KNOCKBACK_STRENGTH = 700

BULLET_SIZE = (100,50)
RELOAD_TIME = .2
ENABLE_SPRAY = True

BULLET_SPEED = {
    'player_test': 1500,
    'enemy_test': 500
}

CAMERA_SHAKE_INTENSITY = 200
ENEMY_DIES_SHAKE_INTENSITY = 500

BULLET_TIME_FACTOR = .15

EVENTS = {
    'player_roll': pygame.USEREVENT + 1
}