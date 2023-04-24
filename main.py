from enemy import Enemy
import pygame, sys,os
from settings import *
from player import Player
from particle import * 
from camera import SpriteGroup3d, CameraGroup
from event_timer import EventTimer


class Tile(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.position = (0,0)

class Game:

    def __init__(self):
        pygame.init()
        cursor_surface = pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'crosshair.png')), 2.5)
        cursor = pygame.cursors.Cursor((10,10), cursor_surface)
        pygame.mouse.set_cursor(cursor)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.timers = []
        
        self.layers = {
            'tiles': SpriteGroup3d(1),
            'bullets': SpriteGroup3d(2),
            'player-particles': ParticleGroup(3),
            'player': SpriteGroup3d(4),
            'enemies': SpriteGroup3d(5),
            'accessories': SpriteGroup3d(6),
            'particles': ParticleGroup(7)
        }

        self.camera = CameraGroup(self)
        
        self.bullet_time = False

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
        self.absolute_mouse_pos = Vector(pygame.mouse.get_pos())
        while run:
            dt = self.get_dt()
            self.events = pygame.event.get()

            self.keys_down = pygame.key.get_pressed()
            self.mouse_buttons = pygame.mouse.get_pressed()
            self.mouse_pos = Vector(pygame.mouse.get_pos())

            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    self.start_bullet_time(1000)
                
                # For ez testing
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    run = False
                    restart = True


            self.screen.fill((50,50,50))
            
            for layer in self.layers.values():
                layer.update(dt)
            
            self.camera.update(dt)
            self.camera.draw()
            self.mouse_pos = self.mouse_pos + self.camera.offset
            
            delete_timers = []
            for timer in self.timers:
                if not timer.update():
                    delete_timers.append(timer)
            for timer in delete_timers:
                self.timers.remove(timer)

            pygame.display.update()
        
        # ez testing
        if restart: 
            self.__init__()
            self.run()
        pygame.quit()
        sys.exit()

    def get_dt(self):
        dt = self.clock.tick(60) / 1000
        if self.bullet_time:
            dt *= BULLET_TIME_FACTOR
        return dt

    def start_bullet_time(self, length = -1):
        self.bullet_time = True
        if length != -1:
            print(length * BULLET_TIME_FACTOR)
            self.timers.append(EventTimer(length * BULLET_TIME_FACTOR, self.end_bullet_time))
        pass

    def end_bullet_time(self):
        self.bullet_time = False
        pass

if __name__ == '__main__':
    game = Game()
    game.run()
