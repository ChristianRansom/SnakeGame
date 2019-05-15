'''
Created on Feb 1, 2019

@author: Christian Ransom
'''
from collections import deque
from game_object import GameObject
import snake_body
import game
import copy

class Snake():
    '''
    classdocs
    '''
    
    def __init__(self, body_length = 0, size = 1, x_value = 0, y_value = 0, direction = "east"):
        '''
        Constructor
        '''
        self.q = deque()
        self.color = (0,128,0) #Green
        self.alive = True
        
        self.head = snake_body.SnakeBody(size, x_value, y_value)
        for _ in range(body_length):
            self.grow(direction)
        
    def collide(self, other):
        return GameObject.collide(self.head, other)
    
    def wall_collide(self, pygame):
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
    
    def die(self, pygame, screen):
        self.color = (128, 0, 0)
        death_sound = pygame.mixer.Sound("Computer Error Alert.wav")
        death_sound.play()
        self.alive = False
    
    def grow(self, direction):
        self.q.append(copy.copy(self.head))
        self.move(direction)
    
    def move(self, direction):
        tail = self.q.popleft()
        move_amount = 1 #It moves 1 tile at a time
        #print("head x " + str(head.x()))
        #print("head y " + str(head.y()))
        #print("tail x " + str(tail.x()))
        #print("tail y " + str(tail.y()))
        
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
            
        self.head = copy.copy(tail)
        self.q.append(tail)
        
    def render(self, screen, pygame, tile_height, tile_width):
        for body in self.q:
            body.render(screen, pygame, self.color, tile_height, tile_width)
            
