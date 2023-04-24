from enemy import Enemy
import pygame, sys
from settings import *
from player import Player
from particle import * 
from camera import SpriteGroup3d, CameraGroup


class Tile(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.position = (0,0)

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.timers = []
        
        self.layers = {
            'tiles': SpriteGroup3d(1),
            'bullets': SpriteGroup3d(2),
            'player-particles': ParticleGroup(3),
            'player': SpriteGroup3d(4),
            'accessories': SpriteGroup3d(5),
            'enemies': SpriteGroup3d(6),
            'particles': ParticleGroup(7)
        }

        self.camera = CameraGroup(self)

        tile = Tile(self.layers['tiles'])
        tile.image = pygame.Surface((50,50))
        tile.image.fill('black')
        tile.rect = tile.image.get_rect()
        tile.rect.center = (100, 200)
        tile.position = tile.rect.center

        enemy = Enemy(self.layers['enemies'], self)
        enemy.position = pygame.math.Vector2((WIN_WIDTH / 3, WIN_HEIGHT / 3))

        self.player = Player(self.layers['player'], self)
    
    def run(self):
        run = True
        restart = False
        while run:
            self.events = pygame.event.get()
            dt = self.clock.tick(60) / 1000

            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # For ez testing
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    run = False
                    restart = True


            self.screen.fill((50,50,50))
            
            for layer in self.layers.values():
                layer.update(dt)
                # layer.draw(self.screen)
            self.camera.draw()
            
            for timer in self.timers:
                timer.update()

            pygame.display.update()
        
        # ez testing
        if restart: 
            self.__init__()
            self.run()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
