import random as r
import time,pygame,sys

width, height = 500, 500
min_width, min_height = 500 // 7, 500 // 7

class Room(pygame.rect.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        self.color = (r.randint(0,255), r.randint(0,255), r.randint(0,255))

def bsp(room_to_split, min_width, min_height):
    rooms_queue = []
    rooms_list = []
    rooms_queue.append(room_to_split)
    while len(rooms_queue) > 0:
        room = rooms_queue.pop(0)
        if room.height >= min_height and room.width >= min_width:
            if r.random() < .5:
                if room.height >= min_height * 2:
                    split_horizontally(room, min_height, rooms_queue)
                elif room.width >= min_width * 2:
                    split_vertically(room, min_width, rooms_queue)
                else:
                    rooms_list.append(room)
            else:
                if room.width >= min_width * 2:
                    split_vertically(room, min_width, rooms_queue)
                elif room.height >= min_height * 2:
                    split_horizontally(room, min_height, rooms_queue)
                else:
                    rooms_list.append(room)
    return rooms_list

def split_horizontally(room, min_height, rooms_queue):
    # split = r.randint(min_height, room.height - min_height)
    split = r.randint(1, room.height)
    top_room = Room(room.left, room.top, room.width, split)
    bottom_room = Room(room.left, room.top + split, room.width, room.height - split)
    rooms_queue.append(top_room)
    rooms_queue.append(bottom_room)

def split_vertically(room, min_width, rooms_queue):
    # split = r.randint(min_width, room.width - min_width)
    split = r.randint(1, room.width)
    left_room = Room(room.left, room.top, split, room.height)
    right_room = Room(room.left + split, room.top, room.width - split, room.height)
    rooms_queue.append(left_room)
    rooms_queue.append(right_room)

rooms = bsp(Room(0, 0, width, height), min_width, min_height)

if __name__ == '__main__':
    pygame.init()
    
    WIN = pygame.display.set_mode((500,500))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(1/3)
        rooms = bsp(Room(0, 0, width, height), min_width, min_height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        WIN.fill('black')
        for room in rooms:
            pygame.draw.rect(WIN, room.color, room)

        pygame.display.update()