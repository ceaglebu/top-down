import pygame,os

def get_image(sheet, gridsize, spritesize, scale, coordinate, offset = (0,0), bg_color='black'):
    # gridsize: size of cell on spritesheet
    # spritesize: size of sprite on spritesheet
    # scale: how much spreadsheet sprite is scaled up to fit box
    image = pygame.Surface(spritesize).convert_alpha()
    image.blit(sheet, (0,0), (coordinate[0] * gridsize[0] + offset[0], coordinate[1] * gridsize[1] + offset[1], spritesize[0], spritesize[1]))
    image = pygame.transform.scale(image, (spritesize[0] * scale, spritesize[1] * scale))
    image.set_colorkey(bg_color)

    return image

def get_animation(sheet, gridsize, spritesize, scale, y_location, start, length, offset = (0,0), bg_color='black'):
    animation = []
    for i in range(length):
        animation.append(get_image(sheet, gridsize, spritesize, scale, (start + i, y_location), offset, bg_color))
    return animation
