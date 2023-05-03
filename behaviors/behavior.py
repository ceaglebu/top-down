from game.settings import FRICTION_STRENGTH, WIN_HEIGHT, WIN_WIDTH
import pygame
from pygame.math import Vector2 as Vector

class Behavior():
    def __init__(self, game, owner):
        self.owner = owner
        self.game = game

    def think(self, dt):
        pass
        
    def move(self, dt):
        pass

    def handle_collision(self):
        pass
    
    def post_collision(self, dt, collide):
        pass


    def behave(self, dt):
        self.think(dt)
        self.move(dt)
        collide = self.handle_collision()
        self.post_collision(dt, collide)

# Default for Moving Objects
class MovingObjectDefaultBehavior(Behavior):
    def __init__(self, game, owner):
        super().__init__(game, owner)

    def think(self, dt):
        pass
        
    def move(self, dt):
        velocity = self.owner.velocity
        phys_velocity = self.owner.phys_velocity
        position = self.owner.position

        self.owner.phys_acceleration = phys_velocity * -FRICTION_STRENGTH
        phys_velocity += self.owner.phys_acceleration * dt

        # If physics velocity is low, set it to 0
        if phys_velocity.magnitude() < 5:
            phys_velocity = Vector()

        # smthn i dont understand
        if phys_velocity.magnitude() >= 30 and self.owner.movement_control.dot(phys_velocity) < 0:
            velocity = phys_velocity + self.owner.movement_control - self.owner.movement_control.dot(phys_velocity.normalize())*(phys_velocity.normalize())
        else:
            velocity = self.owner.movement_control + phys_velocity 
        position += velocity * dt

    def handle_collision(self):
        x_collide = self.handle_x_collision()
        y_collide = self.handle_y_collision()
        return (x_collide, y_collide)


    def handle_x_collision(self):
        rect = self.owner.rect
        velocity = self.owner.velocity
        phys_velocity = self.owner.phys_velocity
        position = self.owner.position
        # Update position to check for collision
        rect.centerx = position.x
        for child in self.owner.child_rects:
            child.centerx = position.x + child.offset.x

        # Check for window border collisions
        if rect.right < 0:
            rect.left = WIN_WIDTH
            position = Vector(rect.center)
        elif rect.left > WIN_WIDTH:
            rect.right = 0
            position = Vector(rect.center)

        # Check for object collisions
        x_collision = False
        for tile in self.game.layers['tiles']:
            if x_collision == False and pygame.Rect.colliderect(tile.rect, self.owner.collision_rect):
                x_collision = True
                if phys_velocity.x * velocity.x > 0:
                    phys_velocity.x = phys_velocity.x * .5
                if velocity.x > 0:
                    rect.right = tile.rect.left + rect.right - self.owner.collision_rect.right
                    position.x = rect.centerx
                elif velocity.x < 0:
                    rect.left = tile.rect.right + rect.left - self.owner.collision_rect.left
                    position.x = rect.centerx
        
        # Move child back if it collided
        for child in self.owner.child_rects:
            child.centerx = position.x + child.offset.x

        return x_collision

    def handle_y_collision(self):
        rect = self.owner.rect
        velocity = self.owner.velocity
        phys_velocity = self.owner.phys_velocity
        position = self.owner.position
        
        rect.centery = position.y
        for child in self.owner.child_rects:
            child.centery = position.y + child.offset.y

        if rect.bottom < 0:
            rect.top = WIN_HEIGHT
            position = Vector(rect.center)
        elif rect.top > WIN_HEIGHT:
            rect.bottom = 0
            position = Vector(rect.center)

        y_collision = False
        for tile in self.game.layers['tiles']:
            if y_collision == False and pygame.Rect.colliderect(tile.rect, self.owner.collision_rect):
                y_collision = True
                if phys_velocity.y * velocity.y > 0:
                    phys_velocity.y = phys_velocity.y * .5
                if velocity.y > 0:
                    rect.bottom = tile.rect.top + rect.bottom - self.owner.collision_rect.bottom
                    position.y = rect.centery
                elif velocity.y < 0:
                    rect.top = tile.rect.bottom + rect.top - self.owner.collision_rect.top
                    position.y = rect.centery

        for child in self.owner.child_rects:
            child.centery = position.y + child.offset.y

        return y_collision
    
    def post_collision(self, dt, collide):
        pass