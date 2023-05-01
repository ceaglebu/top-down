import pygame, sys, os
from settings import *

#####################################################################
# EDITOR CONTROLS:                                                  #
# CTRL + S: save level                                              #
# CTRL + N: new level                                               #
# Z/X: Change tile type (tile types are in levels/settings.py)      #
# CTRL + Arrow Keys: Move all tiles up/down/left/right              #
#####################################################################

# When making levels, fill ground space with white and make walls with black. The rest will be filled in with background color

class Editor:
    def __init__(self, path):
        self.screen = pygame.display.get_surface()
        self.origin = pygame.math.Vector2()

        # Input
        self.mouse_pos = pygame.math.Vector2()
        self.mouse_scroll = 0

        # Pan
        self.mouse_pan_start = pygame.math.Vector2()
        self.origin_pan_start = pygame.math.Vector2()
        self.panning = False

        # Tile selection
        self.tile_size = TILE_SIZE
        self.selected_tile_idx = 0
        self.tiles = pygame.sprite.Group()

        # Level to be edited
        self.path = path
        self.level = []
        self.open_level()

        # Grid
        self.initialize_grid()

        # Gui

    def new_level(self):
        # Create new level
        self.level = []
        for i in range(WIN_HEIGHT // self.tile_size):
            self.level.append([])
            for _ in range(WIN_WIDTH // self.tile_size):
                self.level[i].append(' ')
    
    def open_level(self, temp_file=False):
        # Open level pased on level_num
        
        if temp_file:
            level_file = "temp.txt"
        else:
            level_file = self.path
        try:
            with open(os.path.join('levels', f'{level_file}'), 'r') as level_file:
                self.level = level_file.readlines()
                self.tile_size = int((.9 * WIN_HEIGHT) / len(self.level))
                for i, row in enumerate(self.level):
                    new_row = []
                    new_row[:0] = row.strip('\n')
                    self.level[i] = new_row
                    for x, column in enumerate(self.level[i]):
                        if column != ' ':
                            Tile((x, i), self.tiles, column, self.tile_size)
        except FileNotFoundError:
            self.new_level()
    
    def reload_level(self):
        self.initialize_grid()
        self.tiles = pygame.sprite.Group()

        for i, row in enumerate(self.level):
            for x, column in enumerate(self.level[i]):
                if column != ' ':
                    Tile((x, i), self.tiles, column, self.tile_size)


    def save_level(self):
            # Write tiles to file
            
            with open(os.path.join('levels', f'{self.path}'), 'w') as level_file:
                for line in self.level:
                    for char in line:
                        level_file.write(str(char))
                    level_file.write('\n')
            
            write = ''
            early_file = True
            with open(os.path.join('levels', f'{self.path}'), 'r') as level_file:
                for line in level_file.readlines():
                    if early_file:
                        write += line
                        if not line.isspace():
                            early_file = False
                    elif not line.isspace():
                        write += line
                # level_file.write('test')

            with open(os.path.join('levels', f'{self.path}'), 'w') as level_file:
                level_file.write(write)

    def handle_place(self):
        # Place and remove pieces and extend / shorten level array as necessary
        if self.mouse_input[0]:
            place_posx = int((self.mouse_pos - self.origin).x // self.tile_size)
            place_posy = int((self.mouse_pos - self.origin).y // self.tile_size)
            
            if len(self.level) == 0:
                self.new_level()
            
            if place_posx > len(self.level[0]) - 1:
                for _ in range(place_posx - len(self.level[0]) + 1):
                    for row in self.level:
                        row.append(' ')
            
            if place_posy > len(self.level) - 1:
                for _ in range(place_posy - len(self.level) + 1):
                    self.level.append([' ' for _ in self.level[0]])

            if self.level[place_posy][place_posx] != TILE_TYPES[self.selected_tile_idx][1] and place_posx >= 0 and place_posy >= 0:
                self.level[place_posy][place_posx] = TILE_TYPES[self.selected_tile_idx][1]
                Tile((place_posx, place_posy), self.tiles, TILE_TYPES[self.selected_tile_idx][1], self.tile_size)
            
        elif self.mouse_input[2]:
            place_posx = int((self.mouse_pos - self.origin).x // self.tile_size)
            place_posy = int((self.mouse_pos - self.origin).y // self.tile_size)
            
            if place_posy < len(self.level) and place_posx < len(self.level[0]):
                self.level[place_posy][place_posx] = ' '
            
            for tile in self.tiles:
                if tile.rect.left < self.mouse_pos[0] - self.origin.x < tile.rect.right and tile.rect.top < self.mouse_pos[1] - self.origin.y < tile.rect.bottom:
                    self.tiles.remove(tile)
                    del tile

    def shift_level(self, dir):
        if dir == 'down':
            if len(self.level) != 0:
                self.level.insert(0, [' ' for _ in self.level[0]])
                self.reload_level()
        elif dir == 'up':
            if len(self.level) != 0 and ''.join(self.level[0]).isspace():
                self.level.pop(0)
                self.reload_level()
        elif dir == 'left':
            left_edge = False
            for row in self.level:
                if not row[0].isspace():
                    left_edge = True
            if not left_edge:
                for row in self.level:
                    row.pop(0)
                self.reload_level()
        elif dir == 'right':
            for row in self.level:
                row.insert(0, ' ')
            self.reload_level()

    def handle_shortcuts(self, event):
        if (self.keys_pressed[pygame.K_LCTRL] or self.keys_pressed[pygame.K_RCTRL]):
            if event.key == pygame.K_s:
                self.save_level()
            elif event.key == pygame.K_n:
                self.new_level()
                self.reload_level()
            elif event.key == pygame.K_DOWN:
                self.shift_level('down')
            elif event.key == pygame.K_UP:
                self.shift_level('up')
            elif event.key == pygame.K_LEFT:
                self.shift_level('left')
            elif event.key == pygame.K_RIGHT:
                self.shift_level('right')
            elif event.key == pygame.K_0 or event.key == pygame.K_BACKQUOTE:
                self.origin = pygame.math.Vector2()
        else:
            if event.key == pygame.K_z:
                self.update_selection(-1)
            elif event.key == pygame.K_x:
                self.update_selection(1)
        
    def initialize_grid(self):        
        # Create rectangles to be used in grid
        # Vertical Grid
        self.vertical_grid_lines = []
        for i in range(WIN_WIDTH // self.tile_size + 1): # + 1 is for clipping
            self.vertical_grid_lines.append(pygame.rect.Rect(0, 0, GRID_THICKNESS, WIN_HEIGHT))
            self.centerx = i * self.tile_size

        # Horizontal Grid
        self.horizontal_grid_lines = []
        for i in range(WIN_HEIGHT // self.tile_size + 1):
            self.horizontal_grid_lines.append(pygame.rect.Rect(0, 0, WIN_WIDTH, GRID_THICKNESS))
            self.centery = i * self.tile_size

    def draw_grid(self):
            x_offset = self.origin.x % self.tile_size
            y_offset = self.origin.y % self.tile_size

            # Vertical grid
            for i, line in enumerate(self.vertical_grid_lines):
                line.centerx = x_offset + self.tile_size * i
                pygame.draw.rect(self.screen, GRID_COLOR, line)
            # Horizontal grid
            for i, line in enumerate(self.horizontal_grid_lines):
                line.centery = y_offset + self.tile_size * i
                pygame.draw.rect(self.screen, GRID_COLOR, line)

    def start_pan(self):
        self.mouse_pan_start = self.mouse_pos
        self.origin_pan_start = self.origin
        self.panning = True

    def handle_camera(self):
        
        # Pan
        if self.panning:
            if not self.mouse_input[1]:
                self.panning = False
            
            self.origin = self.origin_pan_start + self.mouse_pos - self.mouse_pan_start

        if self.keys_pressed[pygame.K_LCTRL]:
            if not self.keys_pressed[pygame.K_LALT]:  
                self.origin.x += self.mouse_scroll * PAN_SCROLL_SPEED
            else:
                self.origin.y += self.mouse_scroll * PAN_SCROLL_SPEED

        # Zoom
        if not self.keys_pressed[pygame.K_LCTRL] and self.mouse_scroll != 0 and not (self.mouse_scroll < 1 and self.tile_size < 5):
            self.tile_size += TILE_ZOOM * self.mouse_scroll
            self.reload_level()
            
    def handle_hover(self):
        pass

    def draw_level(self):
        for tile in self.tiles:
            tile.draw_relative(self.screen, self.origin)

    def update_selection(self, move = 1):
        self.selected_tile_idx = (self.selected_tile_idx + move) % len(TILE_TYPES)

    def run(self, clock):
        while True:
            dt = clock.tick(60) / 1000
            events = pygame.event.get()
            # Get Input
            self.keys_pressed = pygame.key.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_input = pygame.mouse.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEWHEEL:
                    self.mouse_scroll = event.y

                if not self.panning and event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:    
                    self.start_pan()
                
                if event.type == pygame.KEYDOWN:
                    self.handle_shortcuts(event)
           
            self.handle_camera()
            self.handle_place()
            self.screen.fill((200,200,200))
            self.draw_grid()
            self.draw_level()
            self.mouse_scroll = 0

            if self.origin.x >= 0:
                pygame.draw.circle(self.screen, 'red', self.origin, 10)
            pygame.display.update()

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, type, tile_size):
        super().__init__(group)
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill(TILE_COLORS[type])
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * tile_size, pos[1] * tile_size)

    def draw_relative(self, surface, origin):
        surface.blit(self.image, (origin.x + self.rect.left, origin.y + self.rect.top))

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("GEARS Gear")
    editor = Editor('1.txt')
    clock = pygame.time.Clock()
    editor.run(clock)
