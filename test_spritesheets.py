from load_sprites import get_animation, get_image
import pygame,sys,os,time

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

sprite_sheet_image = pygame.image.load(os.path.join('assets', 'player', 'mPlayer_ [human].png')).convert_alpha()

clock = pygame.time.Clock()
xRange, yRange = 8, 10
x,y = 0,0
test = [get_image(sprite_sheet_image, 32, 32, (100,100), (0, 0))]
animation = get_animation(sprite_sheet_image, 32, 32, (100,100), 1, 4)
while True:
    clock.tick(6)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        screen.fill((50,50,50))
        screen.blit(animation[0], (0,0))
        screen.blit(animation[1], (32,0))
        screen.blit(animation[2], (64,0))
        screen.blit(test[0], (0,0))

        pygame.display.update() 