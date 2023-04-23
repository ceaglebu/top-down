from enemy import Enemy
import pygame, sys
from settings import *
from player import Player

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.layers = {
            'tiles': pygame.sprite.Group(),
            'bullets': pygame.sprite.Group(),
            'player': pygame.sprite.Group(),
            'accessories': pygame.sprite.Group(),
            'enemies': pygame.sprite.Group()
        }

        tile = pygame.sprite.Sprite(self.layers['tiles'])
        tile.image = pygame.Surface((50,50))
        tile.image.fill('black')
        tile.rect = tile.image.get_rect()
        tile.rect.center = (100, 200)

        enemy = Enemy(self.layers['enemies'], self)
        enemy.position = pygame.math.Vector2((WIN_WIDTH / 3, WIN_HEIGHT / 3))

        self.player = Player(self.layers['player'], self)
    
    def run(self):
        while True:
            self.events = pygame.event.get()
            dt = self.clock.tick(60) / 1000
            
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            self.screen.fill((50,50,50))
            
            for layer in self.layers.values():
                layer.update(dt)
                layer.draw(self.screen)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
