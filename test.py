COLLIDABLE = ['X']
GROUND = ['O', 'E', 'P']
from game.settings import *
def create_level_from_dict(dict):
    level = {}
    for coord, tile_type in dict.items():
        x, y = (int(x) for x in coord.split(','))
        chunk = None
        chunk_coord = (x // CHUNK_SIZE, y // CHUNK_SIZE)
        chunk_string = ','.join(str(e) for e in chunk_coord)
        if chunk_string in level:
            chunk = level[chunk_string]
        else:
            chunk = level[chunk_string] = Chunk()

        group = None
        image = None
        if tile_type in COLLIDABLE:
            group = chunk.walls
            group.append(f'Wall at {coord}')
        elif tile_type in GROUND:
            group = chunk.ground
            group.append(f'Ground at {coord}')
        
        # group.append(Tile(None, self.game, coord, image))

        if tile_type == 'E':
            chunk.spawners.append(f'spawner at {coord}')
    return level

class Chunk:
    def __init__(self):
        self.walls = []
        self.ground = []
        self.enemies = []
        self.spawners = []
    
    def load_chunk(self, level_loader):
        for tile in self.tiles:
            level_loader.game.layers['tiles'].add_internal(tile)
        
        for enemy in self.enemies:
            level_loader.game.layers['enemies'].add_internal(enemy)
        
        for spawner in self.spawners:
            level_loader.spawners.append(spawner)

if __name__ == '__main__':
    dict = {
        '0,0': 'X', '1,0': 'X', '2,0': 'X', '3,0': 'X', '4,0': 'X', '5,0': 'X',
        '0,1': 'X', '1,1': 'O', '2,1': 'O', '3,1': 'O', '4,1': 'O', '5,1': 'X',
        '0,2': 'X', '1,2': 'O', '2,2': 'O', '3,2': 'O', '4,2': 'O', '5,2': 'X',
        '0,3': 'X', '1,3': 'O', '2,3': 'O', '3,3': 'E', '4,3': 'O', '5,3': 'X',
        '0,4': 'X', '1,4': 'O', '2,4': 'O', '3,4': 'O', '4,4': 'O', '5,4': 'X',
        '0,5': 'X', '1,5': 'X', '2,5': 'X', '3,5': 'X', '4,5': 'X', '5,5': 'X',
    }

    level = create_level_from_dict(dict)
    print(level['0,0'].ground)
    print(level['0,0'].spawners)
