from objects.enemies import Grunt
import pygame, sys,os
from game.settings import *
from objects.player import Player
from objects.particle import *
from game.camera import SpriteGroup3d, CameraGroup
from game.event_timer import EventTimer
# from game.level_loader import LevelLoader
from levels.random_level import LevelLoader
from game.sounds import SoundHandler

class Game:

    def __init__(self):
        pygame.init()
        cursor_surface = pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'misc', 'crosshair.png')), 2.5)
        cursor = pygame.cursors.Cursor((10,10), cursor_surface)
        pygame.mouse.set_cursor(cursor)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Fortnite 4")
        self.timers = []
        
        self.layers = {
            'ground': SpriteGroup3d(-1),
            'particles': ParticleGroup(0),
            'tiles': SpriteGroup3d(1),
            'bullets': SpriteGroup3d(2),
            'player-particles': ParticleGroup(3),
            'player': SpriteGroup3d(4),
            'enemies': SpriteGroup3d(4),
            'accessories': SpriteGroup3d(6),
        }

        self.camera = CameraGroup(self)
        self.sound = SoundHandler()
        
        self.bullet_time = False

        self.level_loader = LevelLoader(self)
        # self.level_loader.create_level_from_dict({
        # '0,0': 'X', '1,0': 'X', '2,0': 'X', '3,0': 'X', '4,0': 'X', '5,0': 'X',
        # '0,1': 'X', '1,1': 'O', '2,1': 'O', '3,1': 'O', '4,1': 'O', '5,1': 'X',
        # '0,2': 'X', '1,2': 'O', '2,2': 'E', '3,2': 'O', '4,2': 'O', '5,2': 'X',
        # '0,3': 'X', '1,3': 'O', '2,3': 'P', '3,3': 'O', '4,3': 'O', '5,3': 'X',
        # '0,4': 'X', '1,4': 'O', '2,4': 'O', '3,4': 'O', '4,4': 'O', '5,4': 'X',
        # '0,5': 'X', '1,5': 'X', '2,5': 'X', '3,5': 'X', '4,5': 'X', '5,5': 'X',
        # })
        self.level_loader.load_random_level()

        # self.level_loader = LevelLoader(self)
        self.level_loader.spawn_enemies()

        # self.player = Player(self.layers['player'], self, start_pos=(0,0)) #(WIN_WIDTH // 7, WIN_HEIGHT // 2))
        icon = pygame.transform.chop(self.player.image, (11,12,11,11))
        pygame.display.set_icon(icon)
    
    def run(self):
        run = True
        restart = False
        self.absolute_mouse_pos = Vector(pygame.mouse.get_pos())
        while run:
            dt = self.get_dt()
            self.events = pygame.event.get()

            self.keys_down = pygame.key.get_pressed()
            self.keys_pressed = [0 for _ in range(512)]
            self.mouse_buttons = pygame.mouse.get_pressed()
            self.mouse_pos = Vector(pygame.mouse.get_pos()) + self.player.position - Vector(WIN_WIDTH, WIN_HEIGHT) / 2

            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key < 512:
                        self.keys_pressed[event.key] = 1
                
                # For ez testing
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    run = False
                    restart = True
            
            for layer in self.layers.values():
                layer.update(dt)
            
            self.level_loader.update(dt)
            self.camera.update(dt)
            self.camera.draw()
            self.mouse_pos = self.mouse_pos + self.camera.offset
            
            delete_timers = []
            for timer in self.timers:
                if not timer.update(dt):
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
        dt = self.clock.tick(144) / 1000
        if self.bullet_time:
            dt *= BULLET_TIME_FACTOR
        return dt

    def start_bullet_time(self, length = -1):
        self.bullet_time += 1
        if length != -1:
            self.timers.append(EventTimer(length, self.end_bullet_time))
        pass

    def end_bullet_time(self):
        self.bullet_time -= 1
        pass

if __name__ == '__main__':
    game = Game()
    game.run()
