'''
Created on Jan 29, 2019

@author: Christian Ransom
'''
from gameobject import GameObject

SNAKE_BODY_SIZE = 10

class SnakeBody(GameObject):
    '''
    classdocs
    '''

    #spawns off screen by default
    def __init__(self, xValue = -1000, yValue = -1000):
        '''
        Constructor
        '''
        global SNAKE_BODY_SIZE 
        self.SNAKE_BODY_SIZE = SNAKE_BODY_SIZE
        super().__init__(xValue, yValue)
    
    
    def render(self, screen, pygame, color):
        global SNAKE_BODY_SIZE
        pygame.draw.rect(screen, color, (self.x, self.y,SNAKE_BODY_SIZE,SNAKE_BODY_SIZE), 3)

    
        