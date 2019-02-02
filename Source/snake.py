'''
Created on Feb 1, 2019

@author: Christian Ransom
'''
import game_object
import snake_body
from collections import deque
from game_object import GameObject
import snake_body
import copy

class Snake(GameObject):
    '''
    classdocs
    '''
    
    def __init__(self, body_length, x_value, y_value, direction = "east"):
        '''
        Constructor
        '''
        self.q = deque()
        self.color = (0,128,0) #Green
        self.alive = True
        
        self.head = snake_body.SnakeBody(x_value, y_value)
        for i in range(body_length):
            self.grow(direction)
        
    def collide(self, other):
        return GameObject.collide(self.head, other)
    
    def wall_collide(self, pygame):
        w, h = pygame.display.get_surface().get_size()
        return not (self.head.x >= 0 and self.head.y >= 0 and self.head.x < h and self.head.y < w)

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
    
    def die(self, pygame):
        self.color = (128, 0, 0)
        death_sound = pygame.mixer.Sound("Computer Error Alert.wav")
        death_sound.play()
        self.alive = False
    
    def grow(self, direction):
        new_head = copy.copy(self.head)
        if direction == "east":
            new_head.set_x(self.head.get_x() + 10)
            new_head.set_y(self.head.get_y())
        elif direction == "west":
            new_head.set_x(self.head.get_x() - 10)
            new_head.set_y(self.head.get_y())
        elif direction == "north":
            new_head.set_y(self.head.get_y() - 10)
            new_head.set_x(self.head.get_x())
        elif direction == "south":
            new_head.set_y(self.head.get_y() + 10)
            new_head.set_x(self.head.get_x())
        self.q.append(new_head)
        self.head = new_head
    
    def move(self, direction):
        tail = self.q.popleft()
        #print("head x " + str(head.get_x()))
        #print("head y " + str(head.get_y()))
        #print("tail x " + str(tail.get_x()))
        #print("tail y " + str(tail.get_y()))
        
        #print("north " + str(north) + " south " + str(south) + " east " + str(east) + " west " + str(west))
        
        #Decide the direction of movement
        if direction == "east":
            tail.set_x(self.head.get_x() + 10)
            tail.set_y(self.head.get_y())
        elif direction == "west":
            tail.set_x(self.head.get_x() - 10)
            tail.set_y(self.head.get_y())
        elif direction == "north":
            tail.set_y(self.head.get_y() - 10)
            tail.set_x(self.head.get_x())
        elif direction == "south":
            tail.set_y(self.head.get_y() + 10)
            tail.set_x(self.head.get_x())
            
        self.head = copy.copy(tail)
        self.q.append(tail)
        
    def render(self, screen, pygame):
        for body in self.q:
            body.render(screen, pygame, self.color)
            
