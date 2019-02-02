'''
Created on Feb 1, 2019

@author: Christian Ransom
'''
import gameobject
import snakebody
from collections import deque
from gameobject import GameObject
import snakebody
import copy

class Snake(GameObject):
    '''
    classdocs
    '''
    
    def __init__(self, bodyLength, xValue, yValue, direction = "west"):
        '''
        Constructor
        '''
        self.q = deque()

        self.head = snakebody.SnakeBody(xValue, yValue)
        
        offset = snakebody.SNAKE_BODY_SIZE
        for i in range(bodyLength - 1):
            self.q.append(snakebody.SnakeBody(xValue + offset, yValue))
            offset + snakebody.SNAKE_BODY_SIZE
        
    def move(self, direction):
        tail = self.q.popleft()
        #print("head x " + str(head.getX()))
        #print("head y " + str(head.getY()))
        #print("tail x " + str(tail.getX()))
        #print("tail y " + str(tail.getY()))
        
        #print("north " + str(north) + " south " + str(south) + " east " + str(east) + " west " + str(west))
        
        #Decide the direction of movement
        if direction == "east":
            tail.setX(self.head.getX() + 10)
            tail.setY(self.head.getY())
        elif direction == "west":
            tail.setX(self.head.getX() - 10)
            tail.setY(self.head.getY())
        elif direction == "north":
            tail.setY(self.head.getY() - 10)
            tail.setX(self.head.getX())
        elif direction == "south":
            tail.setY(self.head.getY() + 10)
            tail.setX(self.head.getX())
            
        self.head = copy.copy(tail)
        self.q.append(tail)
        
    def render(self, screen, pygame):
        white = (255,255,255)
        screen.fill(white)
        for aEntity in self.q:
            aEntity.render(screen, pygame)