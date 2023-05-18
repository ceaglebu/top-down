import random as r
from pygame.math import Vector2 as Vector
from game.settings import *

class LevelGenerator:

    def generate_level_dict(self):
        rooms = generate_rooms(1000, 1000, 10, 10, 1)
        hallways = generate_hallways(rooms)

        level_template = {}
        for room in rooms:
            for x in range(room.left, room.left + room.width):
                level_template[f'{x},{room.top}'] = 'X'
                level_template[f'{x},{room.top + room.height - 1}'] = 'X'
                for y in range(room.top + 1, room.top + room.height - 1):
                    if x == room.left or x == room.left + room.width - 1:
                        level_template[f'{x},{y}'] = 'X'
                    else:
                        level_template[f'{x},{y}'] = 'O'
        
        for hallway in hallways:
            if hallway.start[0] != hallway.end[0]:
                # Horizontal hallway
                start, end = sorted([hallway.start[0], hallway.end[0]])
                for x in range(start, end + 1):
                    level_template[f'{x},{hallway.start[1]}'] = 'O'
                    if f'{x},{hallway.start[1] - 1}' not in level_template or level_template[f'{x},{hallway.start[1] - 1}'] not in GROUND:
                        level_template[f'{x},{hallway.start[1] - 1}'] = 'X' 
                    if f'{x},{hallway.start[1] + 1}' not in level_template or level_template[f'{x},{hallway.start[1] + 1}'] not in GROUND:
                        level_template[f'{x},{hallway.start[1] + 1}'] = 'X' 
            else:
                # Vertical hallway
                start, end = sorted([hallway.start[1], hallway.end[1]])
                for y in range(start, end + 1):
                    level_template[f'{hallway.start[0]},{y}'] = 'O'
                    if f'{hallway.start[0] - 1},{y}' not in level_template or level_template[f'{hallway.start[0] - 1},{y}'] not in GROUND:
                        level_template[f'{hallway.start[0] - 1},{y}'] = 'X'
                    if f'{hallway.start[0] + 1},{y}' not in level_template or level_template[f'{hallway.start[0] + 1},{y}'] not in GROUND:
                        level_template[f'{hallway.start[0] + 1},{y}'] = 'X'

        level_template[f'{int(rooms[0].center[0])},{int(rooms[0].center[1])}'] = 'P'
        return level_template

class Room:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.center = (self.left + self.width // 2, self.top + self.height // 2)

class Hallway:
    def __init__(self, start, end):
        self.start = start
        self.end = end

def vertical_split(room, rooms_queue):
    split = r.randint(1, room.width)
    rooms_queue.append(Room(room.left,
                            room.top,
                            split,
                            room.height))
    rooms_queue.append(Room(room.left + split,
                            room.top,
                            room.width - split,
                            room.height))

def horizontal_split(room, rooms_queue):
    split = r.randint(1, room.height)
    rooms_queue.append(Room(room.left,
                            room.top,
                            room.width,
                            split))
    rooms_queue.append(Room(room.left,
                            room.top + split,
                            room.width,
                            room.height - split))

def generate_rooms(space_width, space_height, min_width, min_height, offset):
    rooms_list = []
    rooms_queue = []
    rooms_queue.append(Room(0, 0, space_width, space_height))

    while len(rooms_queue) > 0:
        room = rooms_queue.pop(0)
        if r.randint(0,1) == 1:
            # Split with vertical line
            if room.width >= min_width * 2:
                vertical_split(room, rooms_queue)
            # Split with horizontal line
            elif room.height >= min_height * 2:
                horizontal_split(room, rooms_queue)
            # Don't split, add to list
            elif room.height >= min_height and room.width >= min_width:
                rooms_list.append(room)
        else:
            # Split with horizontal line
            if room.height >= min_height * 2:
                horizontal_split(room, rooms_queue)
            # Split with vertical line
            elif room.width >= min_width * 2:
                vertical_split(room, rooms_queue)
            # Don't split, add to list
            elif room.height >= min_height and room.width >= min_width:
                rooms_list.append(room)
    
    for room in rooms_list:
        room.left += offset
        room.top += offset
        room.width -= offset * 2
        room.height -= offset * 2

    return rooms_list

def generate_hallways(rooms):
    available_rooms = rooms.copy()
    hallways = []

    current_room = available_rooms.pop(0)

    while len(available_rooms) > 0:
        connect_room = None
        for i, room in enumerate(available_rooms):
            if i == 0:
                max_dist = Vector(current_room.center).distance_to(room.center)
                connect_room = room
            else:
                dist = Vector(room.center).distance_to(current_room.center)
                if dist < max_dist:
                    max_dist = dist
                    connect_room = room
        
        if connect_room:
            available_rooms.remove(connect_room)
            if r.randint(0,1) == 0:
                # Have corner on same y axis as start
                hallways.append(Hallway(start= current_room.center, end=(connect_room.center[0], current_room.center[1])))
                hallways.append(Hallway(start= (connect_room.center[0], current_room.center[1]), end= connect_room.center))
            else:
                # Have corner on same x axis as start
                hallways.append(Hallway(start= current_room.center, end= (current_room.center[0], connect_room.center[1])))
                hallways.append(Hallway(start= (current_room.center[0], connect_room.center[1]), end= connect_room.center))
        current_room = connect_room
    return hallways