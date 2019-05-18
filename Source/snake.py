'''
Created on Feb 1, 2019

@author: Christian Ransom
'''
from collections import deque
from game_object import GameObject
import snake_body
import game
import copy
import pygame

class Snake():
    '''
    classdocs
    '''
    
    def __init__(self, body_length = 0, size = 1, x_value = 0, y_value = 0, direction = "east"):
        '''
        Constructor
        '''
        self.q = deque()
        self.head_color = (10,60,10)
        self.alive = True
        self.jumped = False
        
        self.head = snake_body.SnakeBody(size, x_value, y_value)
        for _ in range(body_length):
            self.grow(direction)
        
    def collide(self, other):
        return GameObject.collide(self.head, other)
    
    def wall_collide(self):
        return not (self.head.x >= 0 and self.head.y >= 0 and self.head.x < game.GRID_SIZE and self.head.y < game.GRID_SIZE)

    def self_collide(self):
        #print("================check self collision================")
        #print("Head location")
        #print(self.head.x)
        #print(self.head.y)
        length = len(self.q) #skips the last body since its the head
        i = 0
        for body in self.q:
            #print("body location")
            #print(body.x)
            #print(body.y)
            if i < length - 1:
                if self.head.collide(body) and self.head != body:
                    return True
            i = i + 1
        return False
    
    def die(self, screen, tile_height, tile_width):
        die_color = (128, 0, 0)
        death_sound = pygame.mixer.Sound("Computer Error Alert.wav")
        for body in self.q:
            body.color = die_color
        death_sound.play()
        self.alive = False
    
    def grow(self, direction):
        self.q.append(copy.copy(self.head))
        self.move(direction)
    
    def move(self, direction):
        tail = self.q.popleft()
        move_amount = 1 #It moves 1 tile at a time
        
        #Decide the direction of movement
        if direction == "east":
            tail.x = self.head.x + move_amount
            tail.y = self.head.y
        elif direction == "west":
            tail.x = self.head.x - move_amount
            tail.y = self.head.y
        elif direction == "north":
            tail.y = self.head.y - move_amount
            tail.x = self.head.x
        elif direction == "south":
            tail.y = self.head.y + move_amount
            tail.x = self.head.x
        
        self.q.append(tail)
        self.head = tail
        self.head.color = (0,128,0) #green
        if self.jumped:
            self.head.collider = False
        else:
            self.head.collider = True

    def render(self, screen, tile_height, tile_width):
        jump_color = (0, 0, 255)
        if self.jumped: 
            self.head.color = jump_color
            self.head.collider = False
        for body in self.q:
            body.render(screen, body.color, tile_height, tile_width)
        if not self.jumped: #Render the head a different color
            self.head.render(screen, self.head_color, tile_height, tile_width)
