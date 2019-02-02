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
    
    def __init__(self, bodyLength, xValue, yValue, direction = "east"):
        '''
        Constructor
        '''
        self.q = deque()

        self.head = snakebody.SnakeBody(xValue, yValue)
        
        xValue = xValue - snakebody.SNAKE_BODY_SIZE * (bodyLength)
        
        offset = snakebody.SNAKE_BODY_SIZE
        for i in range(bodyLength - 1):
            #print(offset)
            self.q.append(snakebody.SnakeBody(xValue + offset, yValue))
            offset = offset + snakebody.SNAKE_BODY_SIZE
            
        self.q.append(self.head)
    
    def collide(self, other):
        return GameObject.collide(self.head, other)
    
    def wallCollide(self, pygame):
        w, h = pygame.display.get_surface().get_size()
        return not (self.head.x >= 0 and self.head.y >= 0 and self.head.x < h and self.head.y < w)

    def selfCollide(self):
        #print("================check self collision================")
        #print("Head location")
        #print(self.head.x)
        #print(self.head.y)
        length = len(self.q) #skips the last body since its the head
        i = 0
        for aEntity in self.q:
            #print("body location")
            #print(aEntity.x)
            #print(aEntity.y)
            if i < length - 1:
                if self.head.collide(aEntity) and self.head != aEntity:
                    return True
            i = i + 1
        return False
    
    def grow(self, direction):
        newHead = copy.copy(self.head)
        if direction == "east":
            newHead.setX(self.head.getX() + 10)
            newHead.setY(self.head.getY())
        elif direction == "west":
            newHead.setX(self.head.getX() - 10)
            newHead.setY(self.head.getY())
        elif direction == "north":
            newHead.setY(self.head.getY() - 10)
            newHead.setX(self.head.getX())
        elif direction == "south":
            newHead.setY(self.head.getY() + 10)
            newHead.setX(self.head.getX())
        self.q.append(newHead)
        self.head = newHead
    
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
        for aEntity in self.q:
            aEntity.render(screen, pygame)
            
