import pygame,os

def get_image(sheet, gridsize, spritesize, scale, coordinate, offset = (0,0), bg_color='black'):
    # gridsize: size of cell on spritesheet
    # spritesize: size of sprite on spritesheet
    # scale: how much spreadsheet sprite is scaled up to fit box
    image = pygame.Surface(spritesize).convert_alpha()
    image.blit(sheet, (0,0), (coordinate[0] * gridsize[0] + offset[0], coordinate[1] * gridsize[1] + offset[1], spritesize[0], spritesize[1]))
    image = pygame.transform.scale(image, (spritesize[0] * scale, spritesize[1] * scale))
    image.set_colorkey(bg_color)

    return image.convert()

def get_animation(sheet, gridsize, spritesize, scale, y_location, start, length, offset = (0,0), bg_color='black'):
    animation = []
    for i in range(length):
        animation.append(get_image(sheet, gridsize, spritesize, scale, (start + i, y_location), offset, bg_color))
    return animation

if __name__ == '__main__':
    SPRITESHEETS = {
        'dungeon-floor': pygame.image.load(os.path.join('assets', 'environment', 'dungeon-floor.png')),
        'dungeon-wall': pygame.image.load(os.path.join('assets', 'environment', 'dungeon-wall.png'))
    }
   
    pygame.init()
    WIN = pygame.display.set_mode((500,500))

    test_img = get_image(pygame.image.load(os.path.join('assets', 'misc', 'bullet.png')).convert_alpha(), (16,16), (8,8),  4, (11,9), (5,4)).convert_alpha()
    clock = pygame.time.Clock()

    while True:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        WIN.fill((255,255,255))
        WIN.blit(test_img, (0,0))

        pygame.display.update()